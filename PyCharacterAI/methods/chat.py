import uuid
import json

from typing import Optional, List, Tuple, AsyncGenerator, Any, Union

from ..types import *
from ..exceptions import *


class ChatMethods:
    def __init__(self, client, requester):
        self.__client = client
        self.__requester = requester

    async def fetch_histories(self, character_id: str, amount: int = 50) -> List[ChatHistory]:
        request = await self.__requester.request(
            url="https://plus.character.ai/chat/character/histories/",
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps({
                    "external_id": character_id,
                    "number": amount
                })
            }
        )

        if request.status_code == 200:
            raw_histories = request.json().get('histories', [])
            histories = []

            for raw_history in raw_histories:
                histories.append(ChatHistory(raw_history))

            return histories

        raise FetchError('Cannot fetch histories.')

    async def fetch_chats(self, character_id: str, **kwargs) -> List[Chat]:
        num_preview_turns: int = kwargs.get("num_preview_turns", 2)

        request = await self.__requester.request(
            url=f"https://neo.character.ai/chats/?character_ids={character_id}&num_preview_turns={num_preview_turns}",
            options={
                "headers": self.__client.get_headers(),
            })

        if request.status_code == 200:
            raw_chats = request.json().get('chats', [])
            chats = []

            for raw_chat in raw_chats:
                chats.append(Chat(raw_chat))

            return chats
        raise FetchError('Cannot fetch chats.')

    async def fetch_chat(self, chat_id: str) -> Chat:
        request = await self.__requester.request(
            url=f"https://neo.character.ai/chat/{chat_id}/",
            options={
                "headers": self.__client.get_headers(),
            })

        if request.status_code == 200:
            response = request.json()
            raw_chat = response.get("chat", None)

            if raw_chat:
                return Chat(raw_chat)

        raise FetchError('Cannot fetch chat.')

    async def fetch_recent_chats(self) -> List[Chat]:
        request = await self.__requester.request(
            url=f'https://neo.character.ai/chats/recent/',
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            raw_chats = request.json().get('chats', [])
            chats = []

            for raw_chat in raw_chats:
                chats.append(Chat(raw_chat))
            return chats

        raise FetchError('Cannot fetch recent chats.')

    async def fetch_messages(self, chat_id, pinned_only: bool = False,
                             next_token: str = None) -> Tuple[List[Turn], Optional[str]]:
        url = f"https://neo.character.ai/turns/{chat_id}/"

        if next_token:
            url += f"?next_token={next_token}"

        request = await self.__requester.request(
            url=url,
            options={"headers": self.__client.get_headers()}
        )

        if request.status_code == 200:
            next_token = request.json().get("meta", {}).get("next_token", None)

            raw_turns = request.json().get("turns", [])
            turns = []

            for raw_turn in raw_turns:
                if not pinned_only:
                    turns.append(Turn(raw_turn))
                else:
                    if raw_turn.get("is_pinned", False) is True:
                        turns.append(Turn(raw_turn))

            return turns, next_token
        raise FetchError('Cannot fetch messages.')

    async def fetch_all_messages(self, chat_id, pinned_only: bool = False) -> List[Turn]:
        all_turns = []
        turns, next_token = await self.fetch_messages(chat_id, pinned_only=pinned_only)

        while True:
            if not turns:
                break

            all_turns += turns

            if not next_token:
                break

            turns, next_token = await self.fetch_messages(chat_id, pinned_only=pinned_only, next_token=next_token)

        return all_turns

    async def fetch_pinned_messages(self, chat_id, next_token: str = None) -> [List[Turn], Optional[str]]:
        return await self.fetch_messages(chat_id=chat_id, pinned_only=True, next_token=next_token)

    async def fetch_all_pinned_messages(self, chat_id: str) -> List[Turn]:
        return await self.fetch_all_messages(chat_id=chat_id, pinned_only=True)

    async def fetch_following_messages(self, chat_id: str, turn_id: str, pinned_only: bool = False) -> List[Turn]:
        following_turns = []

        turns, next_token = await self.fetch_messages(chat_id, pinned_only=pinned_only)

        while True:
            if turns is [] or turns is None:
                break

            for turn in turns:
                if turn.turn_id == turn_id:
                    return following_turns

                following_turns.append(turn)

            if next_token is None:
                raise FetchError('Cannot fetch following messages. May be turn_id is invalid?')

            turns, next_token = await self.fetch_messages(chat_id, pinned_only=pinned_only, next_token=next_token)

    async def update_chat_name(self, chat_id: str, name: str) -> bool:
        request = await self.__requester.request(
            url=f'https://neo.character.ai/chat/{chat_id}/update_name',
            options={
                "method": 'PATCH',
                "headers": self.__client.get_headers(),
                "body": json.dumps({"name": name})
            }
        )

        if request.status_code == 200:
            return True

        error_comment = request.json().get("comment")
        raise UpdateError(f'Cannot update chat name. {error_comment}')

    async def archive_chat(self, chat_id: str) -> bool:
        request = await self.__requester.request(
            url=f'https://neo.character.ai/chat/{chat_id}/archive',
            options={
                "method": 'PATCH',
                "headers": self.__client.get_headers(),
                "body": {}
            }
        )

        if request.status_code == 200:
            return True

        raise ActionError(f'Cannot archive chat. Maybe chat is already archived or doesn\'t exist?')

    async def unarchive_chat(self, chat_id: str) -> bool:
        request = await self.__requester.request(
            url=f'https://neo.character.ai/chat/{chat_id}/unarchive',
            options={
                "method": 'PATCH',
                "headers": self.__client.get_headers(),
                "body": {}
            }
        )

        if request.status_code == 200:
            return True

        raise ActionError(f'Cannot unarchive chat. Maybe chat is not archived or doesn\'t exist?')

    async def copy_chat(self, chat_id: str, end_turn_id: str) -> Union[str, None]:
        request = await self.__requester.request(
            url=f'https://neo.character.ai/chat/{chat_id}/copy',
            options={
                "method": 'POST',
                "headers": self.__client.get_headers(),
                "body": json.dumps({
                    "end_turn_id": end_turn_id
                })
            }
        )

        if request.status_code == 200:
            return request.json().get("new_chat_id", None)

        error_comment = request.json().get("comment")
        raise ActionError(f'Cannot copy chat. {error_comment}')

    async def create_chat(self, character_id: str, greeting: bool = True) -> Tuple[Chat, Optional[Turn]]:
        request_id = str(uuid.uuid4())

        request = self.__requester.ws_send({
            'command': 'create_chat',
            'request_id': request_id,
            'payload': {
                'chat': {
                    'chat_id': str(uuid.uuid4()),
                    'creator_id': self.__client.get_account_id(),
                    'visibility': 'VISIBILITY_PRIVATE',
                    'character_id': character_id,
                    'type': 'TYPE_ONE_ON_ONE'
                },
                'with_greeting': greeting
            }
        }, token=self.__client.get_token())

        new_chat: Chat | None = None
        greeting_turn: Turn | None = None

        async for raw_response in request:
            if raw_response['command'] == "create_chat_response":
                new_chat = Chat(raw_response.get("chat", None))
                if greeting:
                    continue
                break

            if raw_response['command'] == "add_turn":
                greeting_turn = Turn(raw_response.get("turn", None))
                break

            if raw_response['command'] == "neo_error":
                await self.__requester.ws_clear(request_id)
                await self.__requester.ws_close()

                error_comment = raw_response.get('comment', '')
                raise CreateError(f'Cannot create a new chat. {error_comment}')

        await self.__requester.ws_clear(request_id)

        if new_chat is None or (greeting is True and greeting_turn is None):
            raise CreateError(f'Cannot create a new chat.')

        return new_chat, greeting_turn

    async def update_primary_candidate(self, chat_id: str, turn_id, candidate_id: str) -> bool:
        ws_message = {
            "command": "update_primary_candidate",
            "origin_id": "web-next",
            "payload": {
                "candidate_id": str(candidate_id),
                "turn_key": {
                    "chat_id": str(chat_id),
                    "turn_id": str(turn_id)
                }
            }
        }

        request = self.__requester.ws_send(ws_message, token=self.__client.get_token())

        async for raw_response in request:
            if raw_response["command"] == "neo_error":
                await self.__requester.ws_close()

                error_comment = raw_response.get('comment', '')
                raise UpdateError(f'Cannot update primary candidate. {error_comment}')

            if raw_response["command"] == "ok":
                break
        return True

    async def send_message(self, character_id: str, chat_id: str, text: str,
                           streaming: bool = False) -> Union[Turn, AsyncGenerator[Turn, Any]]:
        candidate_id = str(uuid.uuid4())
        turn_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())

        ws_message = {
            "command": "create_and_generate_turn",
            "origin_id": "web-next",
            "payload": {
                "character_id": str(character_id),
                "num_candidates": 1,
                "previous_annotations": {
                    "bad_memory": 0,
                    "boring": 0,
                    "ends_chat_early": 0,
                    "funny": 0,
                    "helpful": 0,
                    "inaccurate": 0,
                    "interesting": 0,
                    "long": 0,
                    "not_bad_memory": 0,
                    "not_boring": 0,
                    "not_ends_chat_early": 0,
                    "not_funny": 0,
                    "not_helpful": 0,
                    "not_inaccurate": 0,
                    "not_interesting": 0,
                    "not_long": 0,
                    "not_out_of_character": 0,
                    "not_repetitive": 0,
                    "not_short": 0,
                    "out_of_character": 0,
                    "repetitive": 0,
                    "short": 0
                },
                "selected_language": "",
                "tts_enabled": False,
                "turn": {
                    "author": {
                        "author_id": self.__client.get_account_id(),
                        "is_human": True,
                        "name": ""
                    },
                    "candidates": [
                        {
                            "candidate_id": str(candidate_id),
                            "raw_content": f"{text}"
                        }
                    ],
                    "primary_candidate_id": str(candidate_id),
                    "turn_key": {
                        "chat_id": str(chat_id),
                        "turn_id": str(turn_id)
                    }
                },
                "user_name": ""
            },
            "request_id": str(request_id)
        }

        request = self.__requester.ws_send(ws_message, token=self.__client.get_token())

        async def responses() -> [Turn, Any]:
            try:
                async for raw_response in request:
                    if raw_response["command"] == "neo_error":
                        await self.__requester.ws_clear(request_id)
                        await self.__requester.ws_close()

                        error_comment = raw_response.get("comment", "")
                        raise ActionError(f'Cannot send message. {error_comment}')

                    if raw_response["command"] in ["add_turn", "update_turn"]:
                        # Skip first response
                        if raw_response["turn"].get("author", {}).get("is_human", False):
                            continue

                        yield Turn(raw_response["turn"])

                        if raw_response["turn"].get("candidates")[0].get("is_final", False):
                            break

            finally:
                await self.__requester.ws_clear(request_id)

        if streaming:
            return responses()

        async for response in responses():
            if response.get_primary_candidate().is_final:
                return response

    async def another_response(self, character_id: str, chat_id: str, turn_id: str,
                               streaming: bool = False) -> Union[Turn, AsyncGenerator[Turn, Any]]:
        request_id = str(uuid.uuid4())

        ws_message = {
            "command": "generate_turn_candidate",
            "origin_id": "web-next",
            "payload": {
                "character_id": str(character_id),
                "previous_annotations": {
                    "bad_memory": 0,
                    "boring": 0,
                    "ends_chat_early": 0,
                    "funny": 0,
                    "helpful": 0,
                    "inaccurate": 0,
                    "interesting": 0,
                    "long": 0,
                    "not_bad_memory": 0,
                    "not_boring": 0,
                    "not_ends_chat_early": 0,
                    "not_funny": 0,
                    "not_helpful": 0,
                    "not_inaccurate": 0,
                    "not_interesting": 0,
                    "not_long": 0,
                    "not_out_of_character": 0,
                    "not_repetitive": 0,
                    "not_short": 0,
                    "out_of_character": 0,
                    "repetitive": 0,
                    "short": 0
                },
                "selected_language": "",
                "tts_enabled": False,

                "turn_key": {
                    "chat_id": str(chat_id),
                    "turn_id": str(turn_id)
                },
                "user_name": ""
            },
            "request_id": str(request_id)
        }

        request = self.__requester.ws_send(ws_message, token=self.__client.get_token())

        async def responses() -> [Turn, Any]:
            try:
                async for raw_response in request:
                    if raw_response["command"] == "neo_error":
                        await self.__requester.ws_clear(request_id)
                        await self.__requester.ws_close()

                        error_comment = raw_response.get("comment", "")
                        raise ActionError(f'Cannot generate another response. {error_comment}')

                    if raw_response["command"] == "update_turn":
                        yield Turn(raw_response["turn"])

                        if raw_response["turn"].get("candidates")[0].get("is_final", False):
                            break

            finally:
                await self.__requester.ws_clear(request_id)

        if streaming:
            return responses()

        async for response in responses():
            if response.candidates.get(response.primary_candidate_id).is_final:
                return response

    async def edit_message(self, chat_id: str, turn_id: str, candidate_id: str, text: str) -> Turn:
        request_id = str(uuid.uuid4())

        ws_message = {
            "command": "edit_turn_candidate",
            "request_id": str(request_id),
            "payload": {
                "turn_key": {
                    "chat_id": chat_id,
                    "turn_id": turn_id
                },
                "current_candidate_id": candidate_id,
                "new_candidate_raw_content": text
            },
            "origin_id": "web-next",
        }

        request = self.__requester.ws_send(ws_message, token=self.__client.get_token())

        try:
            async for raw_response in request:
                if raw_response["command"] == "neo_error":
                    await self.__requester.ws_clear(request_id)
                    await self.__requester.ws_close()

                    error_comment = raw_response.get("comment", "")
                    raise EditError(f'Cannot edit message. {error_comment}')

                if raw_response["command"] == "update_turn":
                    return Turn(raw_response["turn"])

        finally:
            await self.__requester.ws_clear(request_id)

    async def delete_messages(self, chat_id: str, turn_ids: List[str]) -> bool:
        request_id = str(uuid.uuid4())

        ws_message = {
            "command": "remove_turns",
            "origin_id": "web-next",
            "payload": {
                "chat_id": str(chat_id),
                "turn_ids": turn_ids
            },
            "request_id": str(request_id)
        }

        request = self.__requester.ws_send(ws_message, token=self.__client.get_token())

        try:
            async for raw_response in request:
                if raw_response["command"] == "neo_error":
                    await self.__requester.ws_clear(request_id)
                    await self.__requester.ws_close()

                    error_comment = raw_response.get("comment", "")
                    raise DeleteError(f'Cannot delete messages. {error_comment}')

                if raw_response["command"] == "remove_turns_response":
                    return True

        finally:
            await self.__requester.ws_clear(request_id)

    async def delete_message(self, chat_id: str, turn_id: str) -> bool:
        return await self.delete_messages(chat_id, [turn_id])

    async def pin_message(self, chat_id: str, turn_id: str) -> bool:
        request_id = str(uuid.uuid4())

        ws_message = {
            "command": "set_turn_pin",
            "origin_id": "web-next",
            "payload": {
                "is_pinned": True,
                "turn_key": {
                    "chat_id": str(chat_id),
                    "turn_id": str(turn_id)
                }
            },
            "request_id": str(request_id)
        }

        request = self.__requester.ws_send(ws_message, token=self.__client.get_token())

        try:
            async for raw_response in request:
                if raw_response["command"] == "neo_error":
                    await self.__requester.ws_clear(request_id)
                    await self.__requester.ws_close()

                    error_comment = raw_response.get("comment", "")
                    raise ActionError(f'Cannot pin message. {error_comment}')

                if raw_response["command"] == "update_turn":
                    if raw_response["turn"].get("is_pinned", False) is True:
                        return True
                    return False

        finally:
            await self.__requester.ws_clear(request_id)

    async def unpin_message(self, chat_id: str, turn_id: str) -> bool:
        request_id = str(uuid.uuid4())

        ws_message = {
            "command": "set_turn_pin",
            "origin_id": "web-next",
            "payload": {
                "is_pinned": False,
                "turn_key": {
                    "chat_id": str(chat_id),
                    "turn_id": str(turn_id)
                }
            },
            "request_id": str(request_id)
        }

        request = self.__requester.ws_send(ws_message, token=self.__client.get_token())

        try:
            async for raw_response in request:
                if raw_response["command"] == "neo_error":
                    await self.__requester.ws_clear(request_id)
                    await self.__requester.ws_close()

                    error_comment = raw_response.get("comment", "")
                    raise ActionError(f'Cannot unpin message. {error_comment}')

                if raw_response["command"] == "update_turn":
                    if raw_response["turn"].get("is_pinned", False) is False:
                        return True
                    return False

        finally:
            await self.__requester.ws_clear(request_id)
