import asyncio
import json

from typing import Dict, AsyncGenerator, Optional, cast

import curl_cffi  # for requests
from curl_cffi.requests import AsyncSession

import aiohttp  # for websockets
from aiohttp import WSMsgType, WSServerHandshakeError

from .exceptions import RequestError, AuthenticationError


class Requester:
    def __init__(self, **kwargs):
        self.__extra_options = kwargs

        self.__impersonate: Optional[str] = self.__extra_options.pop("impersonate", None)

        self.__proxy: Optional[str] = self.__extra_options.pop("proxy", None)

        # whether to create a new websocket session for each new chat on one token
        self.__force_new_ws_session: bool = self.__extra_options.pop("force_new_ws_session", False)

        # debug information (TO-DO)
        self.__debug: bool = self.__extra_options.pop("requester_debug", False)

        self.__requests_session: Optional[curl_cffi.requests.AsyncSession] = None
        self.__ws_sessions: Dict[str, Requester.WebsocketSession] = {}

    # ================================================================== #
    #                              Requests                              #
    # ================================================================== #

    class Response:
        def __init__(
            self,
            url: str,
            status_code: int,
            text: str,
            content: bytes
        ):
            self.url: str = url
            self.status_code: int = status_code
            self.text: str = text
            self.content: bytes = content

        def json(self):
            return json.loads(self.text)

    def requests_session_init(self) -> None:
        self.__requests_session = AsyncSession(
            impersonate=self.__impersonate or "chrome",
            proxy=self.__proxy,
            **self.__extra_options
        )

    async def requests_session_close_async(self) -> None:
        if self.__requests_session is not None:
            await self.__requests_session.close()

    async def request_async(self, url: str, options=None) -> Response:
        if options is None:
            options = {}

        method = options.get("method", "GET")
        headers = options.get("headers", {})
        body = options.get("body", {})

        raw_response: Optional[curl_cffi.requests.Response] = None

        try:
            if method == "GET":
                raw_response = await self.__requests_session.get(url, headers=headers)

            elif method == "POST":
                raw_response = await self.__requests_session.post(url, headers=headers, data=body)

            elif method == "PUT":
                raw_response = await self.__requests_session.put(url, headers=headers, data=body)

            elif method == "PATCH":
                raw_response = await self.__requests_session.patch(url, headers=headers, data=body)

            elif method == "DELETE":
                raw_response = await self.__requests_session.delete(url, headers=headers)

        except curl_cffi.requests.errors.RequestsError:
            raise RequestError

        response = self.Response(url, raw_response.status_code, raw_response.text, raw_response.content)

        if response.status_code == 401:
            raise AuthenticationError("Maybe your token is invalid?")

        return response

    # ================================================================== #
    #                             Websockets                             #
    #              (everything bellow is subject to change)              #
    # ================================================================== #

    class WebsocketSession:
        def __init__(
            self,
            all_sessions: Dict,
            token: str,
            additional_uuid: Optional[str] = None,
            proxy: Optional[str] = None,
            deletion_timeout: float = 60.0,
        ):
            self.token: str = token
            self.additional_uuid: Optional[str] = additional_uuid

            self.session_uuid = f"{token}:{additional_uuid}"

            self.proxy: Optional[str] = proxy

            self.session: Optional[aiohttp.ClientSession] = None
            self.ws: Optional[aiohttp.ClientWebSocketResponse] = None

            self.all_sessions: Dict[str, Requester.WebsocketSession] = all_sessions

            self.response_messages_queue: Optional[asyncio.Queue] = asyncio.Queue()
            self.response_messages: Dict[str, Dict] = {}

            self.receiving: bool = False
            self.receiver_task: Optional[asyncio.Task] = None

            self.in_use: bool = False
            self.deletion_timeout: float = deletion_timeout  # 60 sec by default
            self.deletion_task: Optional[asyncio.Task] = None

            self.all_sessions[self.session_uuid] = self

        @staticmethod
        async def get_session(
            all_sessions: Dict,
            token: str,
            additional_uuid: Optional[str] = None,
            proxy: Optional[str] = None,
            deletion_timeout: float = 60.0
        ):
            session_id = f"{token}:{additional_uuid}"
            session = all_sessions.get(session_id, None)

            if not session:
                session = Requester.WebsocketSession(
                    all_sessions=all_sessions,
                    token=token,
                    additional_uuid=additional_uuid,
                    proxy=proxy,
                    deletion_timeout=deletion_timeout
                )

                await session.init()
            return session

        async def init(self) -> None:
            if self.session or self.ws:
                await self.delete()

            self.session = aiohttp.ClientSession()

            try:
                self.ws = await self.session.ws_connect(
                    url='wss://neo.character.ai/ws/',
                    headers={
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Cookie': f'HTTP_AUTHORIZATION="Token {self.token}"'
                    },
                    proxy=self.proxy,
                    ssl=False
                )

            except WSServerHandshakeError:
                raise AuthenticationError("maybe your token is invalid?")

            self.schedule_deletion()

        @property
        def initialized(self) -> bool:
            return self.session is not None and self.ws is not None

        async def delete(self) -> None:
            self.receiving = False

            if self.receiver_task:
                self.receiver_task.cancel()
                self.receiver_task = None

            if self.ws:
                await self.ws.close()
                self.ws = None

            if self.session:
                await self.session.close()
                self.session = None

            if self.deletion_task:
                self.deletion_task.cancel()
                self.deletion_task = None

            self.all_sessions.pop(self.session_uuid, None)

        def schedule_deletion(self) -> None:
            self.cancel_deletion()

            async def deletion_task() -> None:
                self.in_use = False
                await asyncio.sleep(self.deletion_timeout)

                if not self.in_use:
                    await self.delete()

            self.deletion_task = asyncio.create_task(deletion_task())

        def cancel_deletion(self) -> None:
            self.in_use = True

            if self.deletion_task:
                self.deletion_task.cancel()
                self.deletion_task = None

        async def __receiver(self) -> None:
            while self.receiving:
                response = await self.ws.receive()

                if response.type is WSMsgType.TEXT:
                    response_str = cast(str, response.data)
                    response_json = json.loads(response_str)

                    self.response_messages_queue.put_nowait(response_json)

                elif response.type is WSMsgType.CLOSE:
                    await self.delete()
                    raise RequestError("Connection was closed by server")

                elif response.type is WSMsgType.CLOSING:
                    raise RequestError("Connection is closing")

                elif response.type is WSMsgType.CLOSED:
                    raise RequestError("Connection is closed")

        def __receiver_result_handler(self, task: asyncio.Task):
            try:
                task.result()

            except asyncio.CancelledError:
                pass

            finally:
                self.receiver_task = None
                self.receiving = False

        async def send(self, message: Dict) -> None:
            self.schedule_deletion()

            if not self.initialized:
                await self.init()

            if not self.receiver_task:
                self.receiving = True

                self.receiver_task = asyncio.create_task(self.__receiver())
                self.receiver_task.add_done_callback(self.__receiver_result_handler)

            try:
                await self.ws.send_json(message)

            except ConnectionResetError:
                raise RequestError

        async def receive(self, request_uuid: Optional[str] = None) -> AsyncGenerator:
            self.schedule_deletion()

            try:
                while True:
                    if request_uuid is not None:
                        saved_messages = self.response_messages.get(request_uuid, [])

                        if len(saved_messages) > 0:
                            message = saved_messages.pop(0)
                            self.response_messages[request_uuid] = saved_messages

                            yield message
                            self.schedule_deletion()

                            continue

                    try:
                        current_response = await asyncio.wait_for(self.response_messages_queue.get(), 5)

                    except asyncio.TimeoutError:
                        continue

                    except asyncio.CancelledError:
                        yield None  # signaling that session is closed
                        break

                    command = current_response.get("command", None)

                    if command in [None, "ok"] and request_uuid is None:
                        yield current_response
                        self.schedule_deletion()

                        break

                    messages = self.response_messages.get(request_uuid, [])
                    messages.append(current_response)

                    self.response_messages[request_uuid] = messages

            finally:
                if request_uuid:
                    self.response_messages.pop(request_uuid, None)

        async def send_and_receive(self, message: Dict) -> AsyncGenerator:
            request_uuid = message.get("request_id", None)

            await self.send(message)
            return self.receive(request_uuid)

    async def ws_send_and_receive(self, message: Dict, token: str,
                                  additional_uuid: str = "") -> AsyncGenerator:
        session = await Requester.WebsocketSession.get_session(
            self.__ws_sessions,
            token=token,
            proxy=self.__proxy,
            additional_uuid=additional_uuid if self.__force_new_ws_session else ""
        )

        return await session.send_and_receive(message)

    async def ws_close(self, session_uuid: str):
        session = self.__ws_sessions.get(session_uuid, None)

        if session:
            await session.delete()

    async def ws_close_all(self):
        for session_uuid in list(self.__ws_sessions):
            await self.ws_close(session_uuid)
