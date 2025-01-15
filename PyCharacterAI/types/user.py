from typing import Dict, List, Optional

from .base import BaseCAI
from .media import Avatar
from .character import CharacterShort


class Account(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        account = options.get("account", {})

        self.username: str = options.get("username", "")
        self.name: str = account.get("name", "")
        self.bio: str = options.get("bio", "")

        self.avatar: Optional[Avatar] = None

        avatar_file_name = options.get("avatar_file_name", "")
        if avatar_file_name != "":
            self.avatar = Avatar({"file_name": avatar_file_name})

        self.account_id = options.get("id")
        self.first_name: Optional[str] = options.get("first_name", None)

        self.avatar_type = account.get("avatar_type", "DEFAULT")

        self.is_human = options.get("is_human", True)
        self.email: Optional[str] = options.get("email", None)


class PublicUser(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        self.username: str = options.get("username", "")
        self.name: str = options.get("name", "")
        self.bio: str = options.get("bio", "")

        self.avatar: Optional[Avatar] = None

        avatar_file_name = options.get("avatar_file_name", "")
        if avatar_file_name != "":
            self.avatar = Avatar({"file_name": avatar_file_name})

        self.num_following = options.get("num_following", 0)
        self.num_followers = options.get("num_followers", 0)

        self.characters: List[CharacterShort] = []

        raw_characters = options.get("characters", [])
        if raw_characters != []:
            for raw_character in raw_characters:
                self.characters.append(CharacterShort(raw_character))

        self.subscription_type = options.get("subscription_type", "NONE")


class Persona(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        self.persona_id = options.get("external_id")
        self.name = options.get("participant__name", None) or options.get("name", "")

        self.definition = options.get("definition", "")

        self.avatar: Optional[Avatar] = None

        avatar_file_name = options.get("avatar_file_name", "")
        if avatar_file_name != "":
            self.avatar = Avatar({"file_name": avatar_file_name})

        self.author_username: Optional[str] = options.get("user__username", None)
