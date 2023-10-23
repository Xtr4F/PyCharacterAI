import binascii
import json
import os
from curl_cffi.requests import AsyncSession, Response
import sys, asyncio

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Requester:
    use_plus = False

    def __init__(self, use_plus: bool):
        self.use_plus = use_plus

    class Response:
        def __init__(self, url, code, content):
            self.url = url
            self.status_code = code
            self.content = content

        def json(self):
            return json.loads(self.content)

    async def request(self, url: str, options: dict = {}) -> Response:
        method = options.get('method', 'GET')

        body = options.get('body', {})
        headers = options.get('headers', {})

        response = None

        if self.use_plus:
            url.replace('beta.character.ai', 'plus.character.ai')

        if method == 'GET':
            async with AsyncSession(impersonate="chrome110") as session:
                response = await session.get(url, headers=headers)

        elif method == 'POST':
            async with AsyncSession(impersonate="chrome110") as session:
                response = await session.post(url, headers=headers, data=body)

        elif method == 'PUT':
            async with AsyncSession(impersonate="chrome110") as session:
                response = await session.post(url, headers=headers, data=body)

        if url.endswith("/streaming/"):
            text = response.text.split('\n')[-2]
            return self.Response(url, response.status_code, text)

        return self.Response(url, response.status_code, response.content)

    async def upload_image(self, image: bytes, client, content_type):
        def random_boundary() -> str:
            return binascii.hexlify(os.urandom(16)).decode()

        boundary = f'----WebKitFormBoundary{random_boundary()}'
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'authorization': f"Token {client.get_token()}"
        }

        body = f'--{boundary}\r\n'.encode("UTF-8")
        body += f'Content-Disposition: form-data; name="image"; filename="image"\r\n'.encode("UTF-8")
        body += f'Content-Type: image/{content_type}\r\n\r\n'.encode("UTF-8")
        body += image
        body += f'\r\n--{boundary}--\r\n'.encode("UTF-8")

        request = await self.request("https://beta.character.ai/chat/upload-image/", options={
            "method": 'POST',
            "headers": headers,
            "body": body
        })

        if request.status_code == 200:
            response = request.json()

            if response['status'] == "OK":
                return f"https://characterai.io/i/400/static/user/{response['value']}"

            elif response['status'] == "VIOLATES_POLICY":
                raise Exception("Could not upload an image. Image violates policy.")

        raise Exception("Could not upload an image.")



