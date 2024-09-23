import json
from typing import Union, List

from ...types import PublicUser, Voice
from ...exceptions import FetchError, ActionError
from ...requester import Requester


class UserMethods:
    def __init__(self, client, requester: Requester):
        self.__client = client
        self.__requester = requester

    def fetch_user(self, username: str) -> Union[PublicUser, None]:
        request = self.__requester.request(
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

        raise FetchError('Cannot fetch user.')

    def fetch_user_voices(self, username: str) -> List[Voice]:
        request = self.__requester.request(
            url=f"https://neo.character.ai/multimodal/api/v1/voices/search?creatorInfo.username={username}",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            raw_voices = request.json().get("voices", [])
            voices = []

            for raw_voice in raw_voices:
                voices.append(Voice(raw_voice))

            return voices
        raise FetchError('Cannot fetch user voices.')

    def follow_user(self, username: str) -> bool:
        request = self.__requester.request(
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

        raise ActionError('Cannot follow user.')

    def unfollow_user(self, username: str) -> bool:
        request = self.__requester.request(
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

        raise ActionError('Cannot unfollow user.')
