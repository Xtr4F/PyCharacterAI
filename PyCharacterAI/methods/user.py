import json
from typing import Optional, List, Any

from ..types import PublicUser, Voice
from ..exceptions import FetchError, ActionError

from ..requester import Requester


class UserMethods:
    def __init__(self, client, requester: Requester):
        self.__client = client
        self.__requester = requester

    async def fetch_user(self, username: str, **kwargs: Any) -> Optional[PublicUser]:
        request = await self.__requester.request_async(
            url="https://plus.character.ai/chat/user/public/",
            options={
                "method": "POST",
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps({"username": username}),
            },
        )

        if request.status_code == 200:
            return PublicUser(request.json().get("public_user"))

        if request.status_code == 500:
            return None

        raise FetchError("Cannot fetch user.")

    async def fetch_user_voices(self, username: str, **kwargs: Any) -> List[Voice]:
        request = await self.__requester.request_async(
            url=f"https://neo.character.ai/multimodal/api/v1/voices/search?creatorInfo.username={username}",
            options={"headers": self.__client.get_headers(kwargs.get("token", None))},
        )
        
        response = request.json()

        if request.status_code == 200:
            raw_voices = response.get("voices", [])
            voices = []

            for raw_voice in raw_voices:
                voices.append(Voice(raw_voice))
            return voices

        if response.get("command", "") == "neo_error":
            error_comment = response.get("comment", "")
            raise FetchError(f"Cannot fetch user voices. {error_comment}")
        raise FetchError("Cannot fetch user voices.")

    async def follow_user(self, username: str, **kwargs: Any) -> bool:
        request = await self.__requester.request_async(
            url="https://plus.character.ai/chat/user/follow/",
            options={
                "method": "POST",
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps({"username": username}),
            },
        )

        if request.status_code == 200:
            status = request.json().get("status", "")
            return status == "OK"

        raise ActionError("Cannot follow user.")

    async def unfollow_user(self, username: str, **kwargs: Any) -> bool:
        request = await self.__requester.request_async(
            url="https://plus.character.ai/chat/user/unfollow/",
            options={
                "method": "POST",
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps({"username": username}),
            },
        )

        if request.status_code == 200:
            status = request.json().get("status", "")

            return status == "OK"

        raise ActionError("Cannot unfollow user.")
