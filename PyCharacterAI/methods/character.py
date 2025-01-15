import uuid
import json

from typing import Any, List, Dict, Optional
from urllib.parse import quote

from ..types import Character, CharacterShort
from ..exceptions import (
    FetchError,
    EditError,
    CreateError,
    SearchError,
    ActionError,
    InvalidArgumentError,
)

from ..requester import Requester


class CharacterMethods:
    def __init__(self, client, requester: Requester):
        self.__client = client
        self.__requester = requester

    async def fetch_characters_by_category(self, **kwargs: Any) -> Dict[str, List[CharacterShort]]:
        request = await self.__requester.request_async(
            url="https://plus.character.ai/chat/curated_categories/characters/",
            options={"headers": self.__client.get_headers(kwargs.get("token", None))},
        )

        if request.status_code == 200:
            characters_by_category = {}
            raw = request.json().get("characters_by_curated_category", {})

            for category in raw.keys():
                characters_raw = raw.get(category)
                characters = []

                for character_raw in characters_raw:
                    characters.append(CharacterShort(character_raw))

                characters_by_category[category] = characters

            return characters_by_category

        raise FetchError("Cannot fetch characters by category.")

    async def fetch_recommended_characters(self, **kwargs: Any) -> List[CharacterShort]:
        request = await self.__requester.request_async(
            url="https://neo.character.ai/recommendation/v1/user",
            options={"headers": self.__client.get_headers(kwargs.get("token", None))},
        )

        if request.status_code == 200:
            characters_raw = request.json().get("characters", [])
            characters = []

            for character_raw in characters_raw:
                characters.append(CharacterShort(character_raw))

            return characters

        raise FetchError("Cannot fetch recommended characters.")

    async def fetch_featured_characters(self, **kwargs: Any) -> List[CharacterShort]:
        request = await self.__requester.request_async(
            url="https://plus.character.ai/chat/characters/featured_v2/",
            options={"headers": self.__client.get_headers(kwargs.get("token", None))},
        )

        if request.status_code == 200:
            characters_raw = request.json().get("characters", [])
            characters = []

            for character_raw in characters_raw:
                characters.append(CharacterShort(character_raw))

            return characters

        raise FetchError("Cannot fetch featured characters.")

    async def fetch_similar_characters(self, character_id: str, **kwargs: Any) -> List[CharacterShort]:
        request = await self.__requester.request_async(
            url=f"https://neo.character.ai/recommendation/v1/character/{character_id}",
            options={"headers": self.__client.get_headers(kwargs.get("token", None))},
        )

        if request.status_code == 200:
            characters_raw = request.json().get("characters", [])
            characters = []

            for character_raw in characters_raw:
                characters.append(CharacterShort(character_raw))

            return characters

        raise FetchError("Cannot fetch similar characters.")

    async def fetch_character_info(self, character_id: str, **kwargs: Any) -> Character:
        request = await self.__requester.request_async(
            url="https://plus.character.ai/chat/character/info/",
            options={
                "method": "POST",
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps({"external_id": character_id}),
            },
        )

        if request.status_code == 200:
            response = request.json()
            if response.get("status", "") == "NOT_OK":
                error = response.get("error", "")
                raise FetchError(f"Cannot fetch character information. {error}")

            return Character(response["character"])

        raise FetchError("Cannot fetch character information.")

    async def search_characters(self, character_name: str, **kwargs: Any) -> List[CharacterShort]:
        request = await self.__requester.request_async(
            url=f"https://plus.character.ai/chat/characters/search/?query={quote(character_name)}",
            options={"headers": self.__client.get_headers(kwargs.get("token", None))},
        )

        if request.status_code == 200:
            raw_characters = request.json().get("characters", [])
            return [CharacterShort(raw_character) for raw_character in raw_characters]

        raise SearchError("Cannot search for characters.")

    async def search_creators(self, creator_name: str, **kwargs: Any) -> List[str]:
        request = await self.__requester.request_async(
            url=f"https://plus.character.ai/chat/creators/search/?query={quote(creator_name)}",
            options={"headers": self.__client.get_headers(kwargs.get("token", None))},
        )

        if request.status_code == 200:
            raw_creators = request.json().get("creators")
            return [creator["name"] for creator in raw_creators]

        raise SearchError("Cannot search for creators.")

    async def character_vote(self, character_id: str, vote: Optional[bool], **kwargs: Any) -> bool:
        request = await self.__requester.request_async(
            url="https://plus.character.ai/chat/character/vote/",
            options={
                "method": "POST",
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps({"external_id": character_id, "vote": vote}),
            },
        )

        if request.status_code == 200:
            return (request.json()).get("status", None) == "OK"

        raise ActionError("Cannot vote for character.")

    async def create_character(
        self,
        name: str,
        greeting: str,
        title: str = "",
        description: str = "",
        definition: str = "",
        copyable: bool = False,
        visibility: str = "private",
        avatar_rel_path: str = "",
        default_voice_id: str = "",
        **kwargs: Any,
    ) -> Character:
        if len(name) < 3 or len(name) > 20:
            raise InvalidArgumentError(
                "Cannot create character. Name must be at least 3 characters and no more than 20."
            )

        if len(greeting) < 3 or len(greeting) > 2048:
            raise InvalidArgumentError(
                "Cannot create character. Greeting must be at least 3 characters and no more than 2048."
            )

        visibility = visibility.upper()
        if visibility not in ["UNLISTED", "PUBLIC", "PRIVATE"]:
            raise InvalidArgumentError('Cannot create character. Visibility must be "unlisted", "public" or "private"')

        if title and (len(title) < 3 or len(title) > 50):
            raise InvalidArgumentError(
                "Cannot create character. Title must be at least 3 characters and no more than 50."
            )

        if description and len(description) > 500:
            raise InvalidArgumentError("Cannot create character. Description must be no more than 500 characters.")

        if definition and len(definition) > 32000:
            raise InvalidArgumentError("Cannot create character. Definition must be no more than 32000 characters.")

        request = await self.__requester.request_async(
            url="https://plus.character.ai/chat/character/create/",
            options={
                "method": "POST",
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps(
                    {
                        "avatar_rel_path": avatar_rel_path,
                        "base_img_prompt": "",
                        "categories": [],
                        "copyable": copyable,
                        "default_voice_id": default_voice_id,
                        "definition": definition,
                        "description": description,
                        "greeting": greeting,
                        "identifier": f"id:{str(uuid.uuid4())}",
                        "img_gen_enabled": False,
                        "name": name,
                        "strip_img_prompt_from_msg": False,
                        "title": title,
                        "visibility": visibility,
                        "voice_id": "",
                    }
                ),
            },
        )

        if request.status_code == 200:
            response = request.json()
            if response.get("status", None) == "OK" and response.get("character", None) is not None:
                return Character(response.get("character"))

            raise CreateError(f"Cannot create character. {response.get('error', '')}")

        raise CreateError("Cannot create character.")

    async def edit_character(
        self,
        character_id: str,
        name: str,
        greeting: str,
        title: str = "",
        description: str = "",
        definition: str = "",
        copyable: bool = False,
        visibility: str = "private",
        avatar_rel_path: str = "",
        default_voice_id: str = "",
        **kwargs: Any,
    ) -> Character:
        if len(name) < 3 or len(name) > 20:
            raise InvalidArgumentError("Cannot edit character. Name must be at least 3 characters and no more than 20.")

        if len(greeting) < 3 or len(greeting) > 2048:
            raise InvalidArgumentError(
                "Cannot edit character. Greeting must be at least 3 characters and no more than 2048."
            )

        visibility = visibility.upper()
        if visibility not in ["UNLISTED", "PUBLIC", "PRIVATE"]:
            raise InvalidArgumentError('Cannot edit character. Visibility must be "unlisted", "public" or "private"')

        if title and (len(title) < 3 or len(title) > 50):
            raise InvalidArgumentError(
                "Cannot edit character. Title must be at least 3 characters and no more than 50."
            )

        if description and len(description) > 500:
            raise InvalidArgumentError("Cannot edit character. Description must be no more than 500 characters.")

        if definition and len(definition) > 32000:
            raise InvalidArgumentError("Cannot edit character. Definition must be no more than 32000 characters.")

        request = await self.__requester.request_async(
            url="https://plus.character.ai/chat/character/update/",
            options={
                "method": "POST",
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps(
                    {
                        "archived": False,
                        "avatar_rel_path": avatar_rel_path,
                        "base_img_prompt": "",
                        "categories": [],
                        "copyable": copyable,
                        "default_voice_id": default_voice_id,
                        "definition": definition,
                        "description": description,
                        "external_id": character_id,
                        "greeting": greeting,
                        "img_gen_enabled": False,
                        "name": name,
                        "strip_img_prompt_from_msg": False,
                        "title": title,
                        "visibility": visibility,
                        "voice_id": "",
                    }
                ),
            },
        )

        if request.status_code == 200:
            response = request.json()
            if response.get("status", None) == "OK" and response.get("character", None) is not None:
                return Character(response.get("character"))

            raise EditError(f"Cannot edit character. {response.get('error', '')}")

        raise EditError("Cannot edit character.")
