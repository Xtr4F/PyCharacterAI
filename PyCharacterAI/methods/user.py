import json
from typing import Union, List

from PyCharacterAI.types import *


class UserMethods:
    def __init__(self, client, requester):
        self.__client = client
        self.__requester = requester

    async def fetch_user(self, username: str) -> Union[PublicUser, None]:
        request = await self.__requester.request(
            url='https://plus.character.ai/chat/user/public/', 
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps({'username': username})
            }
        )
        
        if request.status_code == 200:
            return PublicUser(request.json().get('public_user'))
        
        if request.status_code == 500:
            return None

        raise Exception('Cannot fetch user.')

    async def fetch_user_voices(self, username: str) -> List[Voice]:
        request = await self.__requester.request(
            url=f"https://neo.character.ai/multimodal/api/v1/voices/search?creatorInfo.username={username}",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            raw_voices = request.json().get("voices", [])
            voices = []

            for raw_voice in raw_voices:
                voices.append(Voice(raw_voice))

            return voices
        raise Exception('Cannot fetch user voices.')

    async def follow_user(self, username: str) -> bool:
        request = await self.__requester.request(
            url='https://plus.character.ai/chat/user/follow/',
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps({
                    "username": username
                })
            }
        )

        if request.status_code == 200:
            status = request.json().get("status", "")

            if status == "OK":
                return True

        raise Exception('Cannot follow user.')

    async def unfollow_user(self, username: str) -> bool:
        request = await self.__requester.request(
            url='https://plus.character.ai/chat/user/unfollow/',
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps({
                    "username": username
                })
            }
        )

        if request.status_code == 200:
            status = request.json().get("status", "")

            if status == "OK":
                return True

        raise Exception('Cannot unfollow user.')
