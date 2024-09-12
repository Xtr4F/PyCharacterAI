import os
import json

import base64

import mimetypes
from random import randint
from typing import List, Union

from urllib.parse import urlparse

from ..types import *
from ..exceptions import *
from ..requester import Requester


class UtilsMethods:
    def __init__(self, client, requester: Requester):
        self.__client = client
        self.__requester = requester

    async def ping(self) -> bool:
        request = await self.__requester.request(
            url="https://neo.character.ai/ping/",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            return True
        return False

    async def fetch_voice(self, voice_id) -> Voice:
        request = await self.__requester.request(
            url=f"https://neo.character.ai/multimodal/api/v1/voices/{voice_id}",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            return Voice(request.json().get("voice"))

        raise FetchError('Cannot fetch voice. Maybe voice does not exist?')

    async def search_voices(self, voice_name: str) -> List[Voice]:
        request = await self.__requester.request(
            url=f"https://neo.character.ai/multimodal/api/v1/voices/search?query={voice_name}",
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            raw_voices = request.json().get("voices", [])
            return [Voice(raw_voice) for raw_voice in raw_voices]

        raise SearchError('Cannot search for voices.')

    async def generate_image(self, prompt: str, **kwargs) -> List[str]:
        num_candidates: int = kwargs.get("num_candidates", 4)

        request = await self.__requester.request(
            url='https://plus.character.ai/chat/character/generate-avatar-options',
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps(
                    {
                        "prompt": prompt,
                        "num_candidates": num_candidates,
                        "model_version": "v1"
                    }
                )
            })

        if request.status_code == 200:
            response = request.json()
            result = response.get('result', [])

            urls = []

            for img in result:
                url = img.get("url", None)
                if url:
                    urls.append(url)

            return urls
        raise ActionError('Cannot generate image.')

    async def upload_avatar(self, image: str, check_image: bool = True) -> Avatar:
        if os.path.isfile(image):
            with open(image, 'rb') as image_file:
                data = base64.b64encode(image_file.read())

        else:
            parsed_url = urlparse(image)
            if parsed_url.scheme and parsed_url.netloc:
                image_request = await self.__requester.request(image)
                data = base64.b64encode(image_request.content)

            else:
                raise InvalidArgumentError('Cannot upload avatar. Invalid image.')

        mime, _ = mimetypes.guess_type(image)
        image_url = f"data:{mime};base64,{data.decode('utf-8')}"

        request = await self.__requester.request(
            url="https://character.ai/api/trpc/user.uploadAvatar?batch=1",
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(include_web_next_auth=True),
                "body": json.dumps({"0": {"json": {"imageDataUrl": image_url}}})
            }
        )

        if request.status_code == 200:
            response = request.json()[0]

            file_name = ((response.get("result", {})).get("data", {})).get("json", None)
            if file_name is not None:
                avatar = Avatar({"file_name": file_name})

                if check_image:
                    image_request = await self.__requester.request(avatar.get_url())

                    if image_request.status_code != 200:
                        raise UploadError(f"Cannot upload avatar. {image_request.text}")

                return avatar

            raise UploadError("Cannot upload avatar. Maybe your web_next_auth token is invalid, "
                              "or your image is too large, or your image didn't pass the filter.")

    async def upload_voice(self, voice: str, name: str, description: str = "", visibility: str = "private") -> Voice:
        if len(name) < 3 or len(name) > 20:
            raise InvalidArgumentError(f"Cannot upload voice. "
                                       f"Name must be at least 3 characters and no more than 20.")

        if len(description) > 120:
            raise InvalidArgumentError(f"Cannot upload voice. "
                                       f"Description must be no more than 120 characters.")

        visibility = visibility.lower()

        if visibility not in ["private", "public"]:
            raise InvalidArgumentError("Cannot upload voice. "
                                       "Visibility must be \"public\" or \"private\"")

        if os.path.isfile(voice):
            with open(voice, 'rb') as voice_file:
                data = voice_file.read()

        else:
            parsed_url = urlparse(voice)
            if parsed_url.scheme and parsed_url.netloc:
                voice_request = await self.__requester.request(voice)
                data = voice_request.content

            else:
                raise InvalidArgumentError('Cannot upload voice. Invalid audio.')

        mime, _ = mimetypes.guess_type(voice)

        # sequence of 30 random numbers
        boundary = "".join(["{}".format(randint(0, 9)) for _ in range(0, 30)])

        body = f'-----------------------------{boundary}\r\n'.encode("UTF-8")
        body += f'Content-Disposition: form-data; name="file"; filename="input.mp3"\r\n'.encode("UTF-8")
        body += f'Content-Type: {mime}\r\n\r\n'.encode("UTF-8")
        body += data
        body += f"\r\n-----------------------------{boundary}\r\n".encode("UTF-8")
        body += f"Content-Disposition: form-data; name=\"json\"\r\n\r\n".encode("UTF-8")
        body += ('{"voice":{"name":"name","description":"","gender":"neutral","visibility":"private",'
                 '"previewText":"Good day! Here to make life a little less complicated.",'
                 '"audioSourceType":"file"}}\r\n').encode("UTF-8")
        body += f"-----------------------------{boundary}--\r\n".encode("UTF-8")

        # Uploading
        request = await self.__requester.request(
            url="https://neo.character.ai/multimodal/api/v1/voices/",
            options={
                "method": 'POST',
                "headers": {
                    "Content-Type": f"multipart/form-data; boundary=---------------------------{boundary}",
                    "authorization": f"Token {self.__client.get_token()}"
                },
                "body": body
            }
        )

        # Confirming
        if request.status_code in [200, 201]:
            try:
                new_voice = Voice(request.json().get("voice"))
                final_voice = await self.edit_voice(new_voice, name, description, visibility)

                return final_voice

            except Exception:
                raise UploadError("Cannot upload voice.")

        raise UploadError("Cannot upload voice. May be your audio is invalid?")

    async def edit_voice(self, voice: Union[str, Voice], name: str = None, description: str = None,
                         visibility: str = None) -> Voice:
        if not isinstance(voice, Voice):
            voice = await self.fetch_voice(voice)

        if not name:
            name = voice.name

        if not description:
            description = voice.description

        if not visibility:
            visibility = voice.visibility

        if len(name) < 3 or len(name) > 20:
            raise InvalidArgumentError(f"Cannot edit voice. "
                                       f"Name must be at least 3 characters and no more than 20.")

        if len(description) > 120:
            raise InvalidArgumentError(f"Cannot edit voice. "
                                       f"Description must be no more than 120 characters.")

        visibility = visibility.lower()

        if visibility not in ["private", "public"]:
            raise InvalidArgumentError("Cannot edit voice. "
                                       "Visibility must be \"public\" or \"private\"")

        request = await self.__requester.request(
            url=f"https://neo.character.ai/multimodal/api/v1/voices/{voice.voice_id}",
            options={
                "method": 'PUT',
                "headers": self.__client.get_headers(),
                "body": json.dumps(
                    {"voice": {
                          "audioSourceType": "file",
                          "backendId": voice.voice_id,
                          "backendProvider": "cai",
                          "creatorInfo": {"id": voice.creator_id,
                                          "source": "user",
                                          "username": ""},
                          "description": voice.description,
                          "gender": voice.gender,
                          "id": voice.voice_id,
                          "internalStatus": "draft",
                          "lastUpdateTime": "0001-01-01T00:00:00Z",
                          "name": name,
                          "previewAudioURI": voice.preview_audio_url,
                          "previewText": voice.preview_text,
                          "visibility": visibility,
                          }
                     })
            }
        )

        if request.status_code == 200:
            return Voice(request.json().get("voice"))

        raise EditError("Cannot edit voice. May be your audio is invalid?")

    async def delete_voice(self, voice_id: str) -> bool:
        request = await self.__requester.request(
            url=f"https://neo.character.ai/multimodal/api/v1/voices/{voice_id}",
            options={
                "method": "DELETE",
                "headers": self.__client.get_headers()
            }
        )

        if request.status_code == 200:
            return True

        raise DeleteError("Cannot delete voice.")

    async def generate_speech(self, chat_id: str, turn_id: str, candidate_id: str, voice_id: str) -> bytes:
        request = await self.__requester.request(
            url="https://neo.character.ai/multimodal/api/v1/memo/replay",
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps({
                    "candidateId": candidate_id,
                    "roomId": chat_id,
                    "turnId": turn_id,
                    "voiceId": voice_id
                })
            }
        )

        response = request.json()

        if request.status_code != 200:
            error = response.get("error", {}).get("message", "")
            raise ActionError(f"Cannot generate voice. {error}")

        audio_url = response.get("replayUrl", "")

        request = await self.__requester.request(
            url=audio_url,
            options={}
        )

        speech = request.content

        if request.status_code == 200:
            return speech

        raise ActionError("Cannot generate voice.")
