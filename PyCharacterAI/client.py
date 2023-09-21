import base64
import io
import json
import urllib.parse
from io import BytesIO
import requests
import imghdr
import os
from urllib.parse import urlparse

from uuid import uuid4

from PyCharacterAI.chat import Chat
from PyCharacterAI.requester import Requester


class Client:
    __token = None
    __is_guest = True
    __authenticated = False
    __guest_headers = {
        "content-type": "application/json",
        "user-agent": 'CharacterAI/1.0.0 (iPhone; iOS 14.4.2; Scale/3.00)'
    }

    requester = Requester()

    def __init__(self, use_plus: bool = False, headless: bool = True):
        self.requester.use_plus = use_plus
        self.requester.headless = headless

    async def fetch_categories(self) -> list[dict]:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/character/categories/')

        if request.status == 200:
            return (await request.json()).get("categories", [])
        raise Exception('Failed to fetch categories.')

    async def fetch_user_config(self) -> dict:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/config/', options={
            "headers": self.get_guest_headers()
        })

        if request.status == 200:
            return await request.json()
        raise Exception('Failed fetching user configuration.')

    async def fetch_user(self) -> dict:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/user/', options={
            "headers": self.get_headers()
        })

        if request.status == 200:
            return (await request.json()).get("user", {})
        raise Exception('Failed fetching user.')

    async def fetch_featured_characters(self) -> list:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/characters/featured_v2/', options={
            "headers": self.get_headers()
        })

        if request.status == 200:
            return (await request.json()).get('characters', [])
        raise Exception('Failed fetching featured characters.')

    async def fetch_characters_by_category(self, curated: bool = False) -> dict[str, list]:
        if not self.requester.is_initialized():
            raise Exception('You must be authenticated to do this.')

        url = f"https://beta.character.ai/chat/{'curated_categories' if curated else 'categories'}/characters/"

        request = await self.requester.request(url, options={
            "headers": self.get_headers()
        })

        property_ = 'characters_by_curated_category' if curated else 'characters_by_category'

        if request.status == 200:
            return (await request.json())[property_]
        raise Exception('Failed fetching characters by category.')

    async def fetch_character_info(self, character_id: str) -> dict:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request(f"https://beta.character.ai/chat/character/info-cached/{character_id}/",options={
            "headers": self.get_headers()
        })

        if request.status == 200:
            return (await request.json())['character']
        raise Exception('Could not fetch character information.')

    async def search_characters(self, character_name: str) -> list:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')
        if self.is_guest():
            raise Exception('Guest accounts cannot use the search feature.')

        request = await self.requester.request(f"https://beta.character.ai/chat/characters/search/?query={character_name}", options={
            "headers": self.get_headers()
        })

        if request.status == 200:
            return (await request.json()).get('characters')
        raise Exception('Could not search for characters.')

    async def get_recent_conversations(self) -> list:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/characters/recent/', options={
            "headers": self.get_headers()
        })

        if request.status == 200:
            return (await request.json()).get('characters', {})
        raise Exception('Could not get recent conversations.')

    async def generate_image(self, prompt: str) -> str:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/generate-image/', options={
            "method": 'POST',
            "headers": self.get_headers(),
            "body": json.dumps({"image_description": prompt})
        })

        if request.status == 200:
            response = await request.json()
            return response.get('image_rel_path', '')

        raise Exception('Failed generating image.')

    async def upload_image(self, image: str):
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        if os.path.isfile(image):
            with open(image, "rb") as image_file:
                image_data = image_file.read()
        else:
            parsed_url = urlparse(image)
            if parsed_url.scheme and parsed_url.netloc:
                response = requests.get(image)
                image_data = response.content
            else:
                raise Exception('Invalid image format!')

        image_format = imghdr.what(None, h=image_data)

        match image_format:
            case "png":
                image_format = "image/png"
            case "jpeg":
                image_format = "image/jpeg"
            case "webp":
                image_format = "image/webp"
            case _:
                raise Exception('Invalid image format! (Only png, jpeg or webp can be used)')

        base64_img = (base64.b64encode(image_data)).decode('utf-8')

        return await self.requester.upload_image(base64_img, self, image_format)

    async def generate_voice(self, voice_id: int, prompt: str) -> BytesIO | None:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        if self.is_guest():
            raise Exception('Guest accounts cannot generate a voice.')

        text = urllib.parse.quote(prompt)

        if len(text) > 4094:
            raise Exception('Prompt is too long.')

        request = await self.requester.request(f"https://beta.character.ai/chat/character/preview-voice/?voice_id={voice_id}&to_speak={text}", options={
            "method": 'GET',
            "headers": self.get_headers()
        })
        if request.status == 200:
            response = await request.json()

            speech = response['speech']

            if speech == "UklGRiQA/39XQVZFZm10IBAAAAAAAAAAAAAAAAAAAAAAAAAAZGF0YQAA/38=" :
                return None

            binary_data = base64.b64decode(speech)

            audio_stream = io.BytesIO()
            audio_stream.write(binary_data)
            audio_stream.seek(0)

            return audio_stream

        raise Exception("Couldn't generate a voice.")

    async def create_chat(self, character_id: str) -> Chat:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/history/create/', options={
            "method": 'POST',
            "body": json.dumps({
                "character_external_id": character_id
            }),
            "headers": self.get_headers()
        })

        if request.status == 200:
            response = await request.json()
            return Chat(client=self, character_id=character_id, continue_body=response)

        raise Exception('Could not create a new chat.')

    async def continue_chat(self, history_id: str, character_id: str | None = None) -> Chat:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/history/continue/', options={
            "method": 'POST',
            "body": json.dumps({
                "character_external_id": character_id,
                "history_external_id": history_id
            }),
            "headers": self.get_headers()
        })

        if (await request.text()) == "history not found.":
            raise Exception("History not found.")

        if request.status == 200:
            response = await request.json()
            return Chat(client=self, character_id=character_id, continue_body=response)

    async def create_or_continue_chat(self, character_id: str, history_id: str = None) -> Chat:
        if not self.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/history/continue/', options={
            "method": 'POST',
            "body": json.dumps({
                "character_external_id": character_id,
                "history_external_id": history_id
            }),
            "headers": self.get_headers()
        })

        response = None

        if request.status == 404:
            request = await self.requester.request('https://beta.character.ai/chat/history/create/', options={
                "method": 'POST',
                "body": json.dumps({
                    "character_external_id": character_id
                }),
                "headers": self.get_headers()
            })

            if request.status == 200:
                response = await request.json()
            else:
                raise Exception('Could not create a new chat.')

        if request.status == 200:
            response = await request.json()

        return Chat(client=self, character_id=character_id, continue_body=response)

    async def authenticate_with_token(self, token: str):
        if self.is_authenticated():
            raise Exception('Already authenticated')

        await self.requester.initialize() if not self.requester.is_initialized() else None

        request = await self.requester.request('https://beta.character.ai/dj-rest-auth/auth0/', options={
            "method": 'POST',
            "body": {"access_token": token},
            "headers": self.get_guest_headers()
        })

        if request.status == 200:
            response = await request.json()

            self.__is_guest = False
            self.__authenticated = True
            self.__token = response['key']

            return self
        raise Exception('Token is invalid')

    async def authenticate_as_guest(self):
        if self.is_authenticated():
            raise Exception('Already authenticated')

        await self.requester.initialize() if not self.requester.is_initialized() else None

        request = None

        for i in range(20):
            uuid = str(uuid4())
            payload = json.dumps({
                'lazy_uuid': uuid
            })

            request = await self.requester.request('https://beta.character.ai/chat/auth/lazy/', options={
                "method": 'POST',
                "body": payload,
                "headers": self.get_guest_headers()
            })

            if request:
                break

        if request.status == 200:
            response = await request.json()

            if response.get('success') is True:
                self.__is_guest = True
                self.__authenticated = True
                self.__token = response.get('token')

                return self
            else:
                raise Exception('Registering failed')
        else:
            raise Exception('Failed to fetch a lazy token')

    def get_token(self):
        return self.__token

    def is_guest(self):
        return self.__is_guest

    def is_authenticated(self):
        return self.__authenticated

    def get_headers(self):
        return {
            'authorization': f'Token {self.get_token()}',
            'Content-Type': 'application/json'
        }

    def get_guest_headers(self):
        return self.__guest_headers
