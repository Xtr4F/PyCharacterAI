import json
from typing import Union, List

from ...types import PublicUser, Voice
from ...exceptions import FetchError, ActionError
from ...requester import Requester


class UserMethods:
    def __init__(self, client, requester: Requester):
        self.__client = client
        self.__requester = requester

    async def fetch_user(self, username: str, **kwargs) -> Union[PublicUser, None]:
        request = await self.__requester.request_async(
            url='https://plus.character.ai/chat/user/public/', 
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps({'username': username})
            }
        )
        
        if request.status_code == 200:
            return PublicUser(request.json().get('public_user'))
        
        if request.status_code == 500:
            return None

        raise FetchError('Cannot fetch user.')

    async def fetch_user_voices(self, username: str, **kwargs) -> List[Voice]:
        request = await self.__requester.request_async(
            url=f"https://neo.character.ai/multimodal/api/v1/voices/search?creatorInfo.username={username}",
            options={"headers": self.__client.get_headers(kwargs.get("token", None))}
        )

        if request.status_code == 200:
            raw_voices = request.json().get("voices", [])
            voices = []

            for raw_voice in raw_voices:
                voices.append(Voice(raw_voice))

            return voices
        raise FetchError('Cannot fetch user voices.')

    async def follow_user(self, username: str, **kwargs) -> bool:
        request = await self.__requester.request_async(
            url='https://plus.character.ai/chat/user/follow/',
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps({
                    "username": username
                })
            }
        )

        if request.status_code == 200:
            status = request.json().get("status", "")

            if status == "OK":
                return True

        raise ActionError('Cannot follow user.')

    async def unfollow_user(self, username: str, **kwargs) -> bool:
        request = await self.__requester.request_async(
            url='https://plus.character.ai/chat/user/unfollow/',
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(kwargs.get("token", None)),
                "body": json.dumps({
                    "username": username
                })
            }
        )

        if request.status_code == 200:
            status = request.json().get("status", "")

            if status == "OK":
                return True

        raise ActionError('Cannot unfollow user.')
