from datetime import datetime
from typing import Union, List, Dict

from .media import Avatar
from .base import BaseCAI
from .message import Turn, HistoryMessage


# Chat v2
class Chat(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        self.chat_id = options.get("chat_id")
        self.character_id = options.get("character_id")
        self.creator_id = options.get("creator_id")

        create_time = options.get("create_time")

        if create_time:
            try:
                create_time = datetime.strptime(str(create_time), "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                pass

        self.create_time: Union[datetime, None] = create_time

        self.state = options.get("state")
        self.chat_type = options.get("type")

        visibility = options.get("visibility", "public")
        self.visibility = visibility.lower()

        turns = options.get("preview_turns", [])
        self.preview_turns: List[Turn] = [Turn(turn_options) for turn_options in turns]

        self.chat_name: Union[str, None] = options.get("name", None)

        # Some character information:
        self.character_name: Union[str, None] = options.get("character_name", None)
        self.character_avatar: Union[Avatar, None] = None
        avatar_file_name = options.get("character_avatar_uri", "")

        if avatar_file_name != "":
            self.avatar = Avatar({"file_name": avatar_file_name})


# Chat v1
class ChatHistory(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        self.chat_id = options.get("external_id")

        create_time = options.get("created")

        if create_time:
            try:
                create_time = datetime.strptime(str(create_time), "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                pass

        self.create_time: Union[datetime, None] = create_time

        last_interaction = options.get("last_interaction")
        last_interaction = datetime.strptime(last_interaction, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.last_interaction: datetime = last_interaction

        messages = options.get("msgs", [])
        self.preview_messages: List[HistoryMessage] = [HistoryMessage(message) for message in messages]
