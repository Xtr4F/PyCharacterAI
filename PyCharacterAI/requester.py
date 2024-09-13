import json

import websockets

from curl_cffi.requests import AsyncSession

from typing import AsyncGenerator, Dict

import sys
import asyncio

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Requester:
    def __init__(self, **kwargs):
        self.__extra_options = kwargs

        self.__debug = self.__extra_options.pop("requester_debug", False)
        self.__impersonate = self.__extra_options.pop("impersonate", None)

        self.__ws = None
        self.__ws_response_messages = {}

    class Response:
        def __init__(self, url, code, text, content):
            self.url = url
            self.status_code = code
            self.text = text
            self.content = content

        def json(self):
            return json.loads(self.text)

    async def __ws_connect(self, token):
        try:
            cookie = f'HTTP_AUTHORIZATION="Token {token}"'

            self.__ws = await websockets.connect(
                'wss://neo.character.ai/ws/',
                extra_headers={'Cookie': cookie}
            )

        except websockets.exceptions.InvalidStatusCode:
            raise Exception('Invalid token')

    async def ws_clear(self, request_uuid: str = None):
        if request_uuid:
            self.__ws_response_messages.pop(request_uuid, None)
        else:
            self.__ws_response_messages = {}

    async def ws_close(self):
        await self.__ws.close()
        self.__ws = None

    # ============================================= #
    # I don't really know if this method should be so
    # complicated and if what I'm doing is right,
    # so I'm open to your criticism and suggestions,
    # feel free to open a PR.
    # ============================================= #
    async def ws_send(self, message: Dict, token: str) -> AsyncGenerator:
        if self.__ws is None:
            await self.__ws_connect(token)

        request_uuid = message.get("request_id", None)

        await self.__ws.send(json.dumps(message))

        # receiving
        while True:
            if request_uuid is not None:
                saved_messages = self.__ws_response_messages.get(request_uuid, [])

                if len(saved_messages) > 0:
                    message = saved_messages.pop(0)
                    self.__ws_response_messages[request_uuid] = saved_messages

                    yield message
                    continue

            try:
                raw_response = await self.__ws.recv()

            # Reconnecting if connection was closed
            except websockets.exceptions.ConnectionClosed:
                await self.__ws_connect(token)

                # Okay, we're sending message again
                await self.__ws.send(json.dumps(message))
                continue

            response = json.loads(raw_response)

            command = response.get("command", None)

            if command in [None, "ok"] and request_uuid is None:
                yield response
                break

            messages = self.__ws_response_messages.get(request_uuid, [])
            messages.append(response)

            self.__ws_response_messages[request_uuid] = messages

    async def request(self, url: str, options=None) -> Response:
        if options is None:
            options = {}

        method = options.get("method", "GET")
        headers = options.get("headers", {})
        body = options.get("body", {})

        response = None

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

        if self.__debug:
            request = response.request
            print(f"[REQUEST]\n"
                  f"url: {request.url}\n"
                  f"method: {request.method}\n"
                  f"body: {body}\n"
                  f"headers: {request.headers}\n"
                  f"[END OF REQUEST]\n")

            print(f"[RESPONSE]\n"
                  f"status code: {response.status_code}\n"
                  f"text: {response.text}\n"
                  f"[END OF RESPONSE]\n")

        return self.Response(url, response.status_code, response.text, response.content)
