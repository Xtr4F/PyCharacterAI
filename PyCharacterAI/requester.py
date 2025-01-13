import asyncio
import json

from typing import Dict, AsyncGenerator, List, Optional, cast

# for requests
from curl_cffi import requests as curl_cffi_requests

# for websockets
import aiohttp


from .exceptions import RequestError, AuthenticationError


class Requester:
    def __init__(self, **kwargs):
        self.__extra_options = kwargs

        self.__impersonate: Optional[str] = self.__extra_options.pop(
            "impersonate", None
        )

        self.__proxy: Optional[str] = self.__extra_options.pop("proxy", None)

        # debug information (TO-DO)
        self.__debug: bool = self.__extra_options.pop("requester_debug", False)

        self.__ws_session: Optional[aiohttp.ClientSession] = None
        self.__ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.__ws_response_messages: Dict[str, List] = {}

    # ================================================================== #
    #                              Requests                              #
    # ================================================================== #

    class Response:
        def __init__(
            self,
            url: str,
            status_code: int,
            headers: Optional[Dict],
            text: str,
            content: bytes,
        ):
            self.url: str = url
            self.status_code: int = status_code
            self.headers: Optional[Dict] = headers
            self.text: str = text
            self.content: bytes = content

        def json(self):
            return json.loads(self.text)

    async def request_async(self, url: str, options=None) -> Response:
        if options is None:
            options = {}

        method = options.get("method", "GET")
        headers = options.get("headers", {})
        body = options.get("body", {})

        raw_response: Optional[curl_cffi_requests.Response] = None

        try:
            async with curl_cffi_requests.AsyncSession(
                impersonate=self.__impersonate or "chrome",
                proxy=self.__proxy,
                **self.__extra_options,
            ) as session:
                if method == "GET":
                    raw_response = await session.get(url, headers=headers)

                elif method == "POST":
                    raw_response = await session.post(url, headers=headers, data=body)

                elif method == "PUT":
                    raw_response = await session.put(url, headers=headers, data=body)

                elif method == "PATCH":
                    raw_response = await session.patch(url, headers=headers, data=body)

                elif method == "DELETE":
                    raw_response = await session.delete(url, headers=headers)

        except curl_cffi_requests.errors.RequestsError:
            raise RequestError

        if not raw_response:
            raise RequestError

        response = self.Response(
            url=url,
            status_code=raw_response.status_code,
            headers=raw_response.headers,
            text=raw_response.text,
            content=raw_response.content,
        )

        if response.status_code == 401:
            raise AuthenticationError("Maybe your token is invalid?")

        return response

    # ================================================================== #
    #                             Websockets                             #
    #              (everything bellow is subject to change)              #
    # ================================================================== #

    async def ws_close_async(self) -> None:
        if self.__ws:
            try:
                await self.__ws.close()
            finally:
                self.__ws = None

        if self.__ws_session:
            try:
                await self.__ws_session.close()
            finally:
                self.__ws_session = None

    async def __ws_connect_async(self, token: str) -> None:
        if self.__ws_session or self.__ws:
            await self.ws_close_async()

        self.__ws_session = aiohttp.ClientSession()

        try:
            self.__ws = await self.__ws_session.ws_connect(
                url="wss://neo.character.ai/ws/",
                headers={
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36",
                    "Cookie": f'HTTP_AUTHORIZATION="Token {token}"',
                },
                proxy=self.__proxy,
                ssl=False,
            )

        except aiohttp.WSServerHandshakeError:
            raise AuthenticationError("maybe your token is invalid?")

        if not self.__ws_connected:
            raise AuthenticationError("maybe your token is invalid?")

    @property
    def __ws_connected(self) -> bool:
        return self.__ws is not None and self.__ws_session is not None

    async def __ws_ensure_connection(self, token: str) -> None:
        if not self.__ws_connected:
            await self.__ws_connect_async(token=token)

    def __ws_clear_response_messages(self, request_uuid: Optional[str] = None) -> None:
        if request_uuid:
            self.__ws_response_messages.pop(request_uuid, None)
        else:
            self.__ws_response_messages = {}

    async def __ws_send_async(self, message: Dict, token: str) -> None:
        await self.__ws_ensure_connection(token=token)

        try:
            await self.__ws.send_json(message)  # pyright: ignore

        except ConnectionResetError:
            raise RequestError

    async def __ws_receive_async(self, request_uuid: Optional[str]) -> AsyncGenerator:
        try:
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
                    response = await self.__ws.receive()  # pyright: ignore

                    if response.type is aiohttp.WSMsgType.TEXT:
                        response_str = cast(str, response.data)
                        response_json = json.loads(response_str)

                    elif response.type is aiohttp.WSMsgType.CLOSE:
                        await self.ws_close_async()
                        raise RequestError("Connection was closed by server")

                    elif response.type is aiohttp.WSMsgType.CLOSING:
                        raise RequestError("Connection is closing")

                    elif response.type is aiohttp.WSMsgType.CLOSED:
                        raise RequestError("Connection is closed")

                    else:
                        raise RequestError()

                except asyncio.CancelledError:
                    yield None  # signaling that session is closed
                    break

                command = response_json.get("command", None)

                if command in [None, "ok"] or request_uuid is None:
                    yield response_json
                    break

                messages = self.__ws_response_messages.get(request_uuid, [])
                messages.append(response_json)

                self.__ws_response_messages[request_uuid] = messages

        finally:
            if request_uuid:
                self.__ws_clear_response_messages(request_uuid)

    async def ws_send_and_receive_async(
        self, message: Dict, token: str
    ) -> AsyncGenerator:
        request_uuid = message.get("request_id", None)
        await self.__ws_send_async(message=message, token=token)

        try:
            async for message in self.__ws_receive_async(request_uuid=request_uuid):
                yield message

        # Something went wrong. Probably, connection was closed.
        # ! There should be a better way of handling this, feel free to open a PR.

        except RequestError:
            # Okay, let's try again
            await self.__ws_connect_async(token=token)

            await self.__ws_send_async(message=message, token=token)

            async for message in self.__ws_receive_async(request_uuid=request_uuid):
                yield message
