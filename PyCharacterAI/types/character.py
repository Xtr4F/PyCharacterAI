from typing import Dict, Union

from .media import Avatar
from .base import BaseCAI


class CharacterShort(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        self.character_id = options.get("external_id")
        self.title = options.get("title", "")
        self.name = options.get("participant__name", None) or options.get("name", "")

        visibility = options.get("visibility", "public")
        self.visibility = visibility.lower()

        self.greeting = options.get("greeting", "")
        self.description = options.get("description", "")
        self.definition = options.get("definition", "")

        self.upvotes: Union[str, None] = options.get("upvotes", None)

        self.author_username: Union[str, None] = options.get("user__username", None)
        self.num_interactions: Union[str, None] = options.get("participant__num_interactions", None)

        self.avatar: [Avatar, None] = None
        avatar_file_name = options.get("avatar_file_name", "")

        if avatar_file_name != "":
            self.avatar = Avatar({"file_name": avatar_file_name})


class Character(BaseCAI):
    def __init__(self, options: dict):
        super().__init__(options)

        self.character_id = options.get("external_id")
        self.title = options.get("title", "")
        self.name = options.get("participant__name", None) or options.get("name", "")

        visibility = options.get("visibility", "public")
        self.visibility = visibility.lower()

        self.greeting = options.get("greeting", "")
        self.description = options.get("description", "")
        self.definition = options.get("definition", "")

        self.upvotes: Union[str, None] = options.get("upvotes", None)

        self.author_username: Union[str, None] = options.get("user__username", None)
        self.num_interactions: Union[str, None] = options.get("participant__num_interactions", None)

        self.avatar: [Avatar, None] = None
        avatar_file_name = options.get("avatar_file_name", "")

        if avatar_file_name != "":
            self.avatar = Avatar({"file_name": avatar_file_name})

        self.copyable = options.get("copyable", False)
        self.identifier = options.get("identifier", "")

        self.img_gen_enabled = options.get("img_gen_enabled", False)
        self.base_img_prompt = options.get("base_img_prompt", "")
        self.img_prompt_regex = options.get("img_prompt_regex", "")
        self.strip_img_prompt_from_msg = options.get("strip_img_prompt_from_msg", False)
        
        self.starter_prompts = options.get("starter_prompts", {})
        self.comments_enabled = options.get("comments_enabled", False)
        self.internal_id = options.get("participant__user__username", "")
        
        self.voice_id = options.get("voice_id", "")
        self.default_voice_id = options.get("default_voice_id", "")
        self.songs = options.get("songs", [])
