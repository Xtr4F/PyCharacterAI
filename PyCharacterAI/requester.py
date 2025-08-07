import asyncio
import json

from typing import Dict, AsyncGenerator, List, Optional, Tuple

# for requests
import curl_cffi

from .exceptions import RequestError, AuthenticationError, WebsocketClosedError, WebsocketError


class Requester:
    def __init__(self, **kwargs):
        self.__extra_options = kwargs

        self.__websocket_headers: Optional[Dict[str, str]] = self.__extra_options.pop("websocket_headers", None)
        self.__websocket_default_headers: bool = self.__extra_options.pop("websocket_default_headers", True)

        self.__impersonate: Optional[curl_cffi.BrowserTypeLiteral] = self.__extra_options.pop("impersonate", None)
        self.__proxy: Optional[str] = self.__extra_options.pop("proxy", None)

        # debug information (TO-DO)
        # self.__debug: bool = self.__extra_options.pop("requester_debug", False)
        
        self.__requester_session: Optional[curl_cffi.AsyncSession] = None
        self.__ws: Optional[curl_cffi.AsyncWebSocket] = None

        self.__ws_response_messages: Dict[str, List] = {}

    # ================================================================== #
    #                              Requests                              #
    # ================================================================== #

    class Response:
        def __init__(
            self,
            url: str,
            status_code: int,
            headers: List[Tuple[str, str | None]],
            text: str,
            content: bytes,
        ):
            self.url: str = url
            self.status_code: int = status_code
            self.headers: List[Tuple[str, str | None]] = headers
            self.text: str = text
            self.content: bytes = content

        def json(self):
            return json.loads(self.text)
    
    async def open_session(self) -> None: 
        self.__requester_session = curl_cffi.AsyncSession(
            impersonate=self.__impersonate or "firefox135",
            proxy=self.__proxy, 
            **self.__extra_options
        )

    async def close_session(self) -> None:
        if self.__requester_session:
            try:
                await self.__requester_session.close()
            
            finally:
                self.__requester_session = None

    async def ensure_session(self) -> None:
        if not self.__requester_session:
            await self.open_session()

    async def request_async(self, url: str, options=None) -> Response:
        if options is None:
            options = {}

        method = options.get("method", "GET")
        headers = options.get("headers", {})
        cookies = options.get("cookies", {})
        body = options.get("body", {})

        raw_response: Optional[curl_cffi.Response] = None

        await self.ensure_session()
        if not self.__requester_session:
            raise RequestError

        if method == "GET":
            raw_response = await self.__requester_session.get(url, headers=headers, cookies=cookies)

        elif method == "POST":
            raw_response = await self.__requester_session.post(url, headers=headers, data=body, cookies=cookies)

        elif method == "PUT":
            raw_response = await self.__requester_session.put(url, headers=headers, data=body, cookies=cookies)

        elif method == "PATCH":
            raw_response = await self.__requester_session.patch(url, headers=headers, data=body, cookies=cookies)

        elif method == "DELETE":
            raw_response = await self.__requester_session.delete(url, headers=headers, cookies=cookies)


        if not raw_response:
            raise RequestError

        response = self.Response(
            url=url,
            status_code=raw_response.status_code,
            headers=raw_response.headers.multi_items(),
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
            
            except curl_cffi.CurlError:
                raise WebsocketClosedError

            finally:
                self.__ws = None

    async def __ws_connect_async(self, token: str) -> None:
        await self.ensure_session()
        if not self.__requester_session:
            raise RequestError

        if self.__ws:
            await self.ws_close_async()
        
        try:
            self.__ws = await self.__requester_session.ws_connect(
                impersonate="firefox135" or self.__impersonate,
                url="wss://neo.character.ai/ws/",
                headers=self.__websocket_headers,
                default_headers=self.__websocket_default_headers,
                cookies={"HTTP_AUTHORIZATION": f"Token {token}"}
            )

        except curl_cffi.CurlError:
            raise AuthenticationError("maybe your token is invalid?")

        if not self.__ws:
            raise AuthenticationError("maybe your token is invalid?")

    async def __ws_ensure_connection(self, token: str) -> None:
        if not self.__ws:
            await self.__ws_connect_async(token=token)
        
    def __ws_clear_response_messages(self, request_uuid: Optional[str] = None) -> None:
        if request_uuid:
            self.__ws_response_messages.pop(request_uuid, None)
        else:
            self.__ws_response_messages = {}

    async def __ws_send_async(self, message: Dict, token: str) -> None:
        await self.__ws_ensure_connection(token=token)
        
        if not self.__ws:
            raise WebsocketError
        
        try:
            await self.__ws.send_json(message)

        except curl_cffi.CurlError:
            await self.ws_close_async()
            raise WebsocketError


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
                    if not self.__ws:
                        raise WebsocketError

                    try: 
                        response = await self.__ws.recv_str()

                    except curl_cffi.CurlError:
                        await self.ws_close_async()
                        raise WebsocketError
                        
                    response_json = json.loads(response)

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

    async def ws_send_and_receive_async(self, message: Dict, token: str) -> AsyncGenerator:
        request_uuid = message.get("request_id", None)
        retries = 0
        
        while True:
            try:
                await self.__ws_send_async(message=message, token=token)
                async for message in self.__ws_receive_async(request_uuid=request_uuid):
                    yield message
            
            except WebsocketClosedError:
                if retries < 3:
                    retries += 1
                else: 
                    raise RequestError


