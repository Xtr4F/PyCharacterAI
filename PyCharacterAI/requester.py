import json
import time

from typing import Dict, Union, Tuple, Generator, AsyncGenerator

import curl_cffi
from curl_cffi import CurlWsFlag, CurlError, CurlECode
from curl_cffi.requests import AsyncSession, Session, WebSocket


from .exceptions import PyCAIError


class Requester:
    def __init__(self, **kwargs):
        self.__extra_options = kwargs

        self.__impersonate: Union[str, None] = self.__extra_options.pop("impersonate", None)
        self.__debug: bool = self.__extra_options.pop("requester_debug", False)

        self.__ws_session: Union[AsyncSession, Session, None] = None
        self.__ws: Union[WebSocket, None] = None

        self.__ws_response_messages: Dict = {}

# ================================================================== #
#                              Requests                              #
# ================================================================== #

    class Response:
        def __init__(self, url: str, status_code: int, text: str, content: bytes):
            self.url: str = url
            self.status_code: int = status_code
            self.text: str = text
            self.content: bytes = content

        def json(self):
            return json.loads(self.text)

    def request(self, url: str, options=None) -> Response:
        if options is None:
            options = {}

        method = options.get("method", "GET")
        headers = options.get("headers", {})
        body = options.get("body", {})

        response: Union[curl_cffi.requests.Response, None] = None

        with Session(impersonate=self.__impersonate or "chrome", **self.__extra_options) as session:
            if method == "GET":
                response = session.get(url, headers=headers)

            elif method == "POST":
                response = session.post(url, headers=headers, data=body)

            elif method == "PUT":
                response = session.put(url, headers=headers, data=body)

            elif method == "PATCH":
                response = session.patch(url, headers=headers, data=body)

            elif method == "DELETE":
                response = session.delete(url, headers=headers)

        return self.Response(url, response.status_code, response.text, response.content)

    async def async_request(self, url: str, options=None) -> Response:
        if options is None:
            options = {}

        method = options.get("method", "GET")
        headers = options.get("headers", {})
        body = options.get("body", {})

        response: Union[curl_cffi.requests.Response, None] = None

        async with AsyncSession(impersonate=self.__impersonate or "chrome", **self.__extra_options) as session:
            if method == "GET":
                response = await session.get(url, headers=headers)

            elif method == "POST":
                response = await session.post(url, headers=headers, data=body)

            elif method == "PUT":
                response = await session.put(url, headers=headers, data=body)

            elif method == "PATCH":
                response = await session.patch(url, headers=headers, data=body)

            elif method == "DELETE":
                response = await session.delete(url, headers=headers)

        return self.Response(url, response.status_code, response.text, response.content)

# ================================================================== #
#                             Websockets                             #
#              (everything bellow is subject to change)              #
# ================================================================== #

    def __ws_close(self) -> None:
        self.__ws_session.close()

        self.__ws_session = None
        self.__ws = None

    async def __ws_close_async(self) -> None:
        await self.__ws_session.close()

        self.__ws_session = None
        self.__ws = None

    def __ws_connect(self, token) -> None:
        self.__ws_session = Session(impersonate=self.__impersonate or "chrome", **self.__extra_options)

        try:
            self.__ws = self.__ws_session.ws_connect(
                url='wss://neo.character.ai/ws/',
                headers={'Cookie': f'HTTP_AUTHORIZATION="Token {token}"'}
            )

        except CurlError as e:
            self.__ws_close()
            raise PyCAIError(f'{e}\n\nMaybe your token is invalid?')

    async def __ws_connect_async(self, token) -> None:
        self.__ws_session = AsyncSession(impersonate=self.__impersonate or "chrome", **self.__extra_options)

        try:
            self.__ws = await self.__ws_session.ws_connect(
                url='wss://neo.character.ai/ws/',
                headers={'Cookie': f'HTTP_AUTHORIZATION="Token {token}"'}
            )

        except CurlError as e:
            await self.__ws_close_async()
            raise PyCAIError(f'{e}\n\nMaybe your token is invalid?')

    def __ws_receive(self, receive_interval: float = 2) -> Tuple[bytes, int]:
        """
        Receive a frame as bytes.

        libcurl split frames into fragments, so we have to collect all the chunks for
        a frame.
        """

        chunks = []
        flags = 0

        while True:
            try:
                chunk, frame = self.__ws.curl.ws_recv()
                flags = frame.flags

                chunks.append(chunk)

                if frame.bytesleft == 0 and flags & CurlWsFlag.CONT == 0:
                    break

            except CurlError as e:
                if e.code == CurlECode.AGAIN:
                    pass
                else:
                    raise e

            time.sleep(receive_interval)
        return b"".join(chunks), flags

    async def __ws_receive_async(self, receive_interval: float = 0.1) -> Tuple[bytes, int]:
        return await self.__ws.loop.run_in_executor(None, self.__ws_receive)

    def __ws_send(self, payload: bytes, flags: CurlWsFlag = CurlWsFlag.TEXT) -> int:
        """Send a data frame"""
        return self.__ws.curl.ws_send(payload, flags)

    def ws_clear(self, request_uuid: str = None) -> None:
        if request_uuid:
            self.__ws_response_messages.pop(request_uuid, None)
        else:
            self.__ws_response_messages = {}

    def ws_close(self) -> None:
        self.__ws_close()

    async def ws_close_async(self) -> None:
        await self.__ws_close_async()

    # ================================================================= #
    #      I don't really know if the methods bellow should be so       #
    #      complicated and if what I'm doing is right,                  #
    #      so I'm open to your criticism and suggestions,               #
    #      feel free to open a PR.                                      #
    # ================================================================= #

    def ws_send(self, message: Dict, token: str) -> Generator:
        if self.__ws_session is None or self.__ws is None:
            self.__ws_connect(token)

        request_uuid = message.get("request_id", None)

        self.__ws_send(json.dumps(message).encode())

        # receiving
        while True:
            if request_uuid is not None:
                saved_messages = self.__ws_response_messages.get(request_uuid, [])

                if len(saved_messages) > 0:
                    message = saved_messages.pop(0)
                    self.__ws_response_messages[request_uuid] = saved_messages

                    yield message
                    continue

            # else
            try:
                raw_response, flags = self.__ws_receive()

            # something went wrong
            except CurlError as e:

                # reconnecting if connection was closed
                if e.code == 55:
                    self.__ws_connect(token)

                    # Okay, we're sending message again
                    self.__ws_send(json.dumps(message).encode())
                    continue

                else:
                    raise e

            response = json.loads(raw_response.decode())

            command = response.get("command", None)

            if command in [None, "ok"] and request_uuid is None:
                yield response
                break

            messages = self.__ws_response_messages.get(request_uuid, [])
            messages.append(response)

            self.__ws_response_messages[request_uuid] = messages

    async def ws_send_async(self, message: Dict, token: str) -> AsyncGenerator:
        if self.__ws_session is None or self.__ws is None:
            await self.__ws_connect_async(token)

        request_uuid = message.get("request_id", None)

        self.__ws_send(json.dumps(message).encode())

        # receiving
        while True:
            if request_uuid is not None:
                saved_messages = self.__ws_response_messages.get(request_uuid, [])

                if len(saved_messages) > 0:
                    message = saved_messages.pop(0)
                    self.__ws_response_messages[request_uuid] = saved_messages

                    yield message
                    continue

            # else
            try:
                raw_response, flags = await self.__ws_receive_async()

            # something went wrong
            except CurlError as e:

                # reconnecting if connection was closed
                if e.code == 55:
                    await self.__ws_connect_async(token)

                    # Okay, we're sending message again
                    self.__ws_send(json.dumps(message).encode())
                    continue

                else:
                    raise e

            response = json.loads(raw_response.decode())

            command = response.get("command", None)

            if command in [None, "ok"] and request_uuid is None:
                yield response
                break

            messages = self.__ws_response_messages.get(request_uuid, [])
            messages.append(response)

            self.__ws_response_messages[request_uuid] = messages
