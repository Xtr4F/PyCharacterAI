import asyncio

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

        self.__session: Union[Session, AsyncSession, None] = None

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

    def session_init(self) -> None:
        self.__session = None
        self.__session = Session(impersonate=self.__impersonate or "chrome", **self.__extra_options)

    def session_init_async(self) -> None:
        self.__session = None
        self.__session = AsyncSession(impersonate=self.__impersonate or "chrome", **self.__extra_options)

    def session_close(self) -> None:
        if self.__session is not None:
            self.__session.close()

    async def session_close_async(self) -> None:
        if self.__session is not None:
            await self.__session.close()

    def request(self, url: str, options=None) -> Response:
        if options is None:
            options = {}

        method = options.get("method", "GET")
        headers = options.get("headers", {})
        body = options.get("body", {})

        response: Union[curl_cffi.requests.Response, None] = None

        if method == "GET":
            response = self.__session.get(url, headers=headers)

        elif method == "POST":
            response = self.__session.post(url, headers=headers, data=body)

        elif method == "PUT":
            response = self.__session.put(url, headers=headers, data=body)

        elif method == "PATCH":
            response = self.__session.patch(url, headers=headers, data=body)

        elif method == "DELETE":
            response = self.__session.delete(url, headers=headers)

        return self.Response(url, response.status_code, response.text, response.content)

    async def request_async(self, url: str, options=None) -> Response:
        if options is None:
            options = {}

        method = options.get("method", "GET")
        headers = options.get("headers", {})
        body = options.get("body", {})

        response: Union[curl_cffi.requests.Response, None] = None

        if method == "GET":
            response = await self.__session.get(url, headers=headers)

        elif method == "POST":
            response = await self.__session.post(url, headers=headers, data=body)

        elif method == "PUT":
            response = await self.__session.put(url, headers=headers, data=body)

        elif method == "PATCH":
            response = await self.__session.patch(url, headers=headers, data=body)

        elif method == "DELETE":
            response = await self.__session.delete(url, headers=headers)

        return self.Response(url, response.status_code, response.text, response.content)

# ================================================================== #
#                             Websockets                             #
#              (everything bellow is subject to change)              #
# ================================================================== #

    def ws_init(self, token: str) -> None:
        self.__ws = None

        try:
            self.__ws = self.__session.ws_connect(
                url='wss://neo.character.ai/ws/',
                headers={'Cookie': f'HTTP_AUTHORIZATION="Token {token}"'}
            )

            if not self.__ws:
                raise PyCAIError("Cannot connect to websocket.")

        except CurlError as e:
            raise PyCAIError(f'{e}\n\nMaybe your token is invalid?')

    async def ws_init_async(self, token: str) -> None:
        self.__ws = None

        try:
            self.__ws = await self.__session.ws_connect(
                url='wss://neo.character.ai/ws/',
                headers={'Cookie': f'HTTP_AUTHORIZATION="Token {token}"'}
            )

            if not self.__ws:
                raise PyCAIError("Cannot connect to websocket.")

        except CurlError as e:
            raise PyCAIError(f'{e}\n\nMaybe your token is invalid?')

    def ws_close(self):
        if self.__ws:
            self.__ws.close()
            self.__ws = None

    async def ws_close_async(self):
        if self.__ws:
            self.__ws.close()
            self.__ws = None

    def ws_clear(self, request_uuid: str = None) -> None:
        if request_uuid:
            self.__ws_response_messages.pop(request_uuid, None)
        else:
            self.__ws_response_messages = {}

    def ws_receive(self, receive_interval: float = 0.1) -> Tuple[bytes, int]:
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

    async def ws_receive_async(self, receive_interval: float = 0.1) -> Tuple[bytes, int]:
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

            await asyncio.sleep(receive_interval)
        return b"".join(chunks), flags

    def __ws_send(self, payload: bytes, flags: CurlWsFlag = CurlWsFlag.TEXT) -> int:
        return self.__ws.curl.ws_send(payload, flags)

    # ================================================================= #
    #      I don't really know if the methods bellow should be so       #
    #      complicated and if what I'm doing is right,                  #
    #      so I'm open to your criticism and suggestions,               #
    #      feel free to open a PR.                                      #
    # ================================================================= #

    def ws_send(self, message: Dict, token: str) -> Generator:
        if self.__ws is None:
            self.ws_init(token)

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
                raw_response, flags = self.ws_receive()

            # something went wrong
            except CurlError as e:

                # reconnecting if connection was closed
                if e.code == 55:
                    self.ws_init(token)

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
        if self.__ws is None:
            await self.ws_init_async(token)

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
                raw_response, flags = await self.ws_receive_async()

            # something went wrong
            except CurlError as e:

                # reconnecting if connection was closed
                if e.code == 55:
                    await self.ws_init_async(token)

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
