import uuid
import json
from typing import List, Dict, Union

from PyCharacterAI.types import *
from PyCharacterAI.requester import Requester


class AccountMethods:
    def __init__(self, client, requester: Requester):
        self.__client = client
        self.__requester = requester

    async def fetch_me(self) -> Account:
        request = await self.__requester.request(
            url='https://plus.character.ai/chat/user/',
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            return Account(request.json().get('user').get('user'))
        
        raise Exception('Cannot fetch your account.')

    async def fetch_my_settings(self) -> Dict:
        request = await self.__requester.request(
            url="https://plus.character.ai/chat/user/settings/",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            return request.json()

        raise Exception('Cannot fetch your settings.')

    async def fetch_my_followers(self) -> List:
        request = await self.__requester.request(
            url='https://plus.character.ai/chat/user/followers/',
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            return request.json().get("followers", [])

        raise Exception('Cannot fetch your followers.')

    async def fetch_my_following(self) -> List:
        request = await self.__requester.request(
            url='https://plus.character.ai/chat/user/following/',
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            return request.json().get("following", [])

        raise Exception('Cannot fetch your following.')

    async def fetch_my_persona(self, persona_id: str) -> Persona:
        request = await self.__requester.request(
            url=f"https://plus.character.ai/chat/persona/?id={persona_id}",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            persona = request.json().get("persona", None)
            if persona:
                return Persona(persona)

        raise Exception('Cannot fetch your persona. May be persona does not exist?')

    async def fetch_my_personas(self) -> List[Persona]:
        request = await self.__requester.request(
            url="https://plus.character.ai/chat/personas/?force_refresh=1",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            raw_personas = request.json().get("personas", [])
            personas = []

            for raw_persona in raw_personas:
                personas.append(Persona(raw_persona))

            return personas

        raise Exception('Cannot fetch your personas.')

    async def fetch_my_characters(self) -> List[CharacterShort]:
        request = await self.__requester.request(
            url="https://plus.character.ai/chat/characters/?scope=user",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            raw_characters = request.json().get("characters", [])
            characters = []

            for raw_character in raw_characters:
                characters.append(CharacterShort(raw_character))

            return characters

        raise Exception('Cannot fetch your characters.')

    async def fetch_my_upvoted_characters(self) -> List[CharacterShort]:
        request = await self.__requester.request(
            url=f'https://plus.character.ai/chat/user/characters/upvoted/',
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            characters_raw = request.json().get('characters', [])
            characters = []

            for character_raw in characters_raw:
                characters.append(CharacterShort(character_raw))
            return characters

        raise Exception('Cannot fetch your upvoted characters.')

    async def fetch_my_voices(self) -> List[Voice]:
        request = await self.__requester.request(
            url=f"https://neo.character.ai/multimodal/api/v1/voices/user",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            raw_voices = request.json().get("voices", [])
            voices = []

            for raw_voice in raw_voices:
                voices.append(Voice(raw_voice))

            return voices
        raise Exception('Cannot fetch your voices.')

    async def __update_settings(self, options: Dict) -> Dict:
        default_persona_id = options.get("default_persona_id", None)
        persona_override = options.get("persona_override", None)
        voice_override = options.get("voice_override", None)
        character_id = options.get("character_id", None)

        if default_persona_id is None and persona_override is None and voice_override is None:
            raise Exception('Cannot update account settings')

        settings = await self.fetch_my_settings()

        if default_persona_id is not None:
            settings["default_persona_id"] = default_persona_id

        if persona_override is not None and character_id is not None:
            persona_overrides = settings.get("personaOverrides", {})
            persona_overrides[character_id] = persona_override

            settings["personaOverrides"] = persona_overrides

        request = await self.__requester.request(
            url="https://plus.character.ai/chat/user/update_settings/",
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps(settings)
            }
        )

        if request.status_code == 200:
            response = request.json()

            if response.get("success", False):
                return response.get("settings")

        raise Exception('Cannot update account settings')

    async def edit_account(self, name: str, username: str, bio: str = "", avatar_rel_path: str = "") -> bool:
        if len(username) < 2 or len(name) > 20:
            raise Exception(f"Cannot edit account info. Username must be at least 2 characters and no more than 20.")

        if len(name) < 2 or len(name) > 50:
            raise Exception(f"Cannot edit account info. Name must be at least 2 characters and no more than 50.")

        if len(bio) > 500:
            raise Exception(f"Cannot edit account info. Bio must be no more than 500 characters.")

        new_account_info = {
            "avatar_type": "UPLOADED" if avatar_rel_path else "DEFAULT",
            "bio": bio,
            "name": name,
            "username": username
        }

        if avatar_rel_path:
            new_account_info["avatar_rel_path"] = avatar_rel_path

        request = await self.__requester.request(
            url='https://plus.character.ai/chat/user/update/',
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps(new_account_info)
            }
        )

        if request.status_code == 200:
            status = request.json().get("status", "")

            if status == "OK":
                return True

            raise Exception(f"Cannot edit account info {status}")
        raise Exception('Cannot edit account info')

    async def create_persona(self, name: str, definition: str = "", avatar_rel_path: str = "") -> Persona:
        if len(name) < 3 or len(name) > 20:
            raise Exception(f"Cannot create persona. Name must be at least 3 characters and no more than 20.")

        if definition and len(definition) > 728:
            raise Exception(f"Cannot create persona. Definition must be no more than 728 characters.")

        request = await self.__requester.request(
            url=f"https://plus.character.ai/chat/character/create/",
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps({
                    "avatar_file_name": "",
                    "avatar_rel_path": avatar_rel_path,
                    "base_img_prompt": "",
                    "categories": [],
                    "copyable": False,
                    "definition": definition,
                    "description": "This is my persona.",
                    "greeting": "Hello! This is my persona",
                    "identifier": f"id:{str(uuid.uuid4())}",
                    "img_gen_enabled": False,
                    "name": name,
                    "strip_img_prompt_from_msg": False,
                    "title": name,
                    "visibility": "PRIVATE",
                    "voice_id": ""
                })
            }
        )

        if request.status_code == 200:
            response = request.json()
            if response.get("status", None) == "OK" and response.get("persona", None) is not None:
                return Persona(response.get("persona"))

            raise Exception(f"Cannot create persona. {response.get("error", "")}")
        raise Exception(f"Cannot create persona.")

    async def edit_persona(self, persona_id: str, name: str = "", definition: str = "",
                           avatar_rel_path: str = "") -> Persona:
        if name and (len(name) < 3 or len(name) > 20):
            raise Exception(f"Cannot edit persona. Name must be at least 3 characters and no more than 20.")

        if definition and len(definition) > 728:
            raise Exception(f"Cannot edit persona. Definition must be no more than 728 characters.")

        try:
            old_persona = await self.fetch_my_persona(persona_id)
        except Exception:
            raise Exception("Cannot edit persona. May be persona does not exist?")

        payload = {
                    "avatar_file_name": old_persona.avatar.get_file_name() if old_persona.avatar else "",
                    "avatar_rel_path": old_persona.avatar.get_file_name() if old_persona.avatar else "",
                    "copyable": False,
                    "default_voice_id": "",
                    "definition": definition or old_persona.definition,
                    "description": "This is my persona.",
                    "enabled": False,
                    "external_id": persona_id,
                    "greeting": "Hello! This is my persona",
                    "img_gen_enabled": False,
                    "is_persona": True,
                    "name": name or old_persona.name,
                    "participant__name": name or old_persona.name,
                    "participant__num_interactions": 0,
                    "title": name,
                    "user__id": self.__client.get_account_id(),
                    "user__username": old_persona.author_username,
                    "visibility": "PRIVATE"
        }

        if avatar_rel_path:
            payload["avatar_file_name"] = avatar_rel_path
            payload["avatar_rel_path"] = avatar_rel_path

        request = await self.__requester.request(
            url=f"https://plus.character.ai/chat/persona/update/",
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps(payload)
            }
        )

        if request.status_code == 200:
            response = request.json()
            if response.get("status", None) == "OK" and response.get("persona", None) is not None:
                return Persona(response.get("persona"))

            raise Exception(f"Cannot edit persona. {response.get("error", "")}")
        raise Exception(f"Cannot edit persona.")

    async def delete_persona(self, persona_id: str) -> bool:
        try:
            old_persona = await self.fetch_my_persona(persona_id)
        except Exception:
            raise Exception("Cannot delete persona. May be persona does not exist?")

        payload = {
            "archived": True,
            "avatar_file_name": old_persona.avatar.get_file_name() if old_persona.avatar else "",
            "copyable": False,
            "default_voice_id": "",
            "definition": old_persona.definition,
            "description": "This is my persona.",
            "external_id": persona_id,
            "greeting": "Hello! This is my persona",
            "img_gen_enabled": False,
            "is_persona": True,
            "name": old_persona.name,
            "participant__name": old_persona.name,
            "participant__num_interactions": 0,
            "title": old_persona.name,
            "user__id": self.__client.get_account_id(),
            "user__username": old_persona.author_username,
            "visibility": "PRIVATE"
        }

        request = await self.__requester.request(
            url=f"https://plus.character.ai/chat/persona/update/",
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps(payload)
            }
        )

        if request.status_code == 200:
            response = request.json()
            if response.get("status", None) == "OK" and response.get("persona", None) is not None:
                return True

            raise Exception(f"Cannot delete persona. {response.get("error", "")}")
        raise Exception(f"Cannot delete persona.")

    async def set_default_persona(self, persona_id: Union[str, None]) -> bool:
        try:
            if persona_id is None:
                persona_id = ""

            await self.__update_settings({"default_persona_id": persona_id})
            return True
        except Exception:
            raise Exception(f"Cannot set default persona.")

    async def unset_default_persona(self) -> bool:
        return await self.set_default_persona(None)

    async def set_persona(self, character_id: str, persona_id: Union[str, None]) -> bool:
        try:
            if persona_id is None:
                persona_id = ""

            await self.__update_settings({
                    "persona_override": persona_id,
                    "character_id": character_id
            })
            return True
        except Exception:
            raise Exception(f"Cannot set persona.")
    
    async def unset_persona(self, character_id: str) -> bool:
        return await self.set_persona(character_id, None)

    async def set_voice(self, character_id: str, voice_id: Union[str, None]) -> bool:
        method = "update" if voice_id else "delete"

        request = await self.__requester.request(
            url=f"https://plus.character.ai/chat/character/{character_id}/voice_override/{method}/",
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps({"voice_id": voice_id}) if voice_id else None
            }
        )

        if request.status_code == 200:
            if (request.json()).get("success", False):
                return True

        raise Exception(f"Cannot set voice.")

    async def unset_voice(self, character_id: str) -> bool:
        return await self.set_voice(character_id, None)
