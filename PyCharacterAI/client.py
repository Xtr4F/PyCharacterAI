import json

from uuid import uuid4

from PyCharacterAI.chat import Chat
from PyCharacterAI.requester import Requester


class Client:
    _token = None
    _is_guest = True
    _authenticated = False
    _guest_headers = {
        "content-type": "application/json",
        "user-agent": 'CharacterAI/1.0.0 (iPhone; iOS 14.4.2; Scale/3.00)'
    }

    requester = Requester()

    def __init__(self):
        pass

    async def fetch_categories(self) -> list[dict]:
        if not self._authenticated:
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/character/categories/')

        if request.status == 200:
            return (await request.json()).get("categories", [])
        raise Exception('Failed to fetch categories.')

    async def fetch_user_config(self) -> dict:
        if not self._authenticated:
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/config/', options={
            "headers": self._guest_headers
        })

        if request.status == 200:
            return await request.json()
        raise Exception('Failed fetching user configuration.')

    async def fetch_user(self) -> dict:
        if not self._authenticated:
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/user/', options={
            "headers": dict(self.get_headers())
        })

        if request.status == 200:
            return (await request.json()).get("user", {})
        raise Exception('Failed fetching user.')

    async def fetch_featured_characters(self) -> list:
        if not self._authenticated:
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
        if not self._authenticated:
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request(f"https://beta.character.ai/chat/character/info-cached/{character_id}/",options={
            "headers": self.get_headers()
        })

        if request.status == 200:
            return (await request.json())['character']
        raise Exception('Could not fetch character information.')

    async def search_characters(self, character_name: str) -> list:
        if not self._authenticated:
            raise Exception('You must be authenticated to do this.')
        if self._is_guest:
            raise Exception('Guest accounts cannot use the search feature.')

        request = await self.requester.request(f"https://beta.character.ai/chat/characters/search/?query={character_name}", options={
            "headers": self.get_headers()
        })

        if request.status == 200:
            return (await request.json()).get('characters')
        raise Exception('Could not search for characters.')

    async def get_recent_conversations(self) -> list:
        if not self._authenticated:
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/characters/recent/', options={
            "headers": self.get_headers()
        })

        if request.status == 200:
            return (await request.json()).get('characters', {})
        raise Exception('Could not get recent conversations.')

    async def create_chat(self, character_id: str) -> Chat:
        if not self._authenticated:
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

    async def continue_chat(self, character_id: str, history_id: str) -> Chat:
        if not self._authenticated:
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
        if not self._authenticated:
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
            "headers": self._guest_headers
        })

        if request.status == 200:
            response = await request.json()

            self._is_guest = False
            self._authenticated = True
            self._token = response['key']

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
                "headers": self._guest_headers
            })

            if request:
                break

        if request.status == 200:
            response = await request.json()

            if response.get('success') is True:
                self._is_guest = True
                self._authenticated = True
                self._token = response.get('token')

                return self
            else:
                raise Exception('Registering failed')
        else:
            raise Exception('Failed to fetch a lazy token')

    def get_token(self):
        return self._token

    def is_guest(self):
        return self._is_guest

    def is_authenticated(self):
        return self._authenticated

    def get_headers(self):
        return {
            'authorization': f'Token {self._token}',
            'Content-Type': 'application/json'
        }
