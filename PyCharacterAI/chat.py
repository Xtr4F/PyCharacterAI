import json
from typing import Any, Dict, Literal, Optional, Union

from PyCharacterAI.message import Message, MessageHistory, OutgoingMessage, Reply


class Chat:
    def __init__(self, client, character_id: str, continue_body: dict):
        self.character_id = character_id
        self.history_id = continue_body.get('external_id')

        self.client = client

        ai = next(participant for participant in continue_body.get('participants') if not participant['is_human'])

        self.ai_id = ai['user']['username']
        self.requester = client.requester

    async def fetch_history(self, page_num: int = None) -> MessageHistory:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        page_string = f"&page_num={page_num}" if page_num else ""
        url = f"https://beta.character.ai/chat/history/msgs/user/?history_external_id={self.history_id}{page_string}"

        request = await self.requester.request(url, options={
            "headers": self.client.get_headers()
        })

        if request.status == 200:
            response = await request.json()

            history_messages = response['messages']
            messages = []

            for i in range(len(history_messages)):
                message = history_messages[i]
                message["pos_in_history"] = i + 1

                messages.append(Message(chat=self, options=message))

            has_more = response.get("has_more", False)
            next_page = response.get("next_page", None)

            return MessageHistory(chat=self, messages=messages, has_more=has_more, next_page=next_page)

        raise Exception('Could not fetch the chat history.')

    async def get_histories(self, amount: int = 50) -> list:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/character/histories/', options={
            "method": 'POST',
            "headers": self.client.get_headers(),
            "body": json.dumps({
                "external_id": self.character_id,
                "number": amount
            })
        })

        if request.status == 200:
            response = await request.json()

            return response.get('histories', {})

        raise Exception('Failed to fetch stories')

    async def start_new_chat(self) -> dict:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/history/create/', options={
            "method": 'POST',
            "headers": self.client.get_headers(),
            "body": json.dumps({
                "character_external_id": self.character_id
            })
        })

        if request.status == 200:
            response = await request.json()

            self.history_id = response.get('external_id', self.history_id)

            return response

        raise Exception('Failed creating new chat.')

    async def send_to_character(self, options: dict) -> Reply:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        payload = OutgoingMessage(chat=self, options=options).get_payload()

        request = await self.requester.request('https://beta.character.ai/chat/streaming/', options={
            "method": 'POST',
            "headers": self.client.get_headers(),
            "body": json.dumps(payload),
            "client": self.client
        })

        if request.get('status', 500) == 200:
            response = json.loads(request.get('text', {}))

            replies = response.get("replies", [])

            messages = []

            for i in range(len(replies)):
                messages.append(Reply(chat=self, options=response))

            if len(messages) == 0:
                return []

            return messages.pop()
        raise Exception('Failed sending request to character.')

    async def send_message(self, text: str = "", primary_msg_uuid=None, image_path=None, image_description=None) -> Reply:
        options = {
            "text": text
        }

        if primary_msg_uuid:
            options['primary_msg_uuid'] = primary_msg_uuid

        if image_path:
            options["image_rel_path"] = image_path
            options["image_description"] = image_description or ""
            options["image_description_type"] = "HUMAN" if image_description else "AUTO_IMAGE_CAPTIONING"

        return await self.send_to_character(options)

    async def another_response(self, parent_msg_uuid) -> Reply:
        return await self.send_to_character(options={'parent_msg_uuid': parent_msg_uuid})

    async def generate_image(self, prompt: str) -> str:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        request = await self.requester.request('https://beta.character.ai/chat/generate-image/', options={
            "method": 'POST',
            "headers": self.client.get_headers(),
            "body": json.dumps({"image_description": prompt})
        })

        if request.status == 200:
            response = await request.json()

            return response.get('image_rel_path', '')

        raise Exception('Failed generating image.')

    async def change_to_conversation(self, history_id: str, force: bool = False) -> bool:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        if force:
            self.history_id = history_id
        else:
            conversations = await self.get_histories()

            for i in range(len(conversations)):
                conversation = conversations[i]
                if conversation.get('external_id', '') == history_id:
                    self.history_id = history_id
                    return True

            raise Exception("Could not switch to conversation, it either doesn't exist or is invalid.")

    async def get_message(self, message_uuid: str) -> Message | None:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        history = await self.fetch_history()
        history_messages = history.messages

        for i in range(len(history_messages)):
            message = history_messages[i]

            if message.uuid == message_uuid:
                return message

        return None

    async def get_following_messages(self, message_uuid: str, only_uuids: bool = True) -> list[Message | str] | None:
        messages = []

        start_message: Message = await self.get_message(message_uuid)
        if start_message is None:
            return None

        history = await self.fetch_history()
        history_messages = history.messages

        print(len(history_messages))

        if len(history_messages) > start_message.pos_in_history:
            for i in range(start_message.pos_in_history, len(history_messages) + 1):
                print(i)
                message = history_messages[i - 1]
                messages.append(message)

        else:
            messages.append(start_message)

        if only_uuids:
            uuids = []
            for message in messages:
                uuids.append(message.uuid)
            return uuids
        else:
            return messages

    async def get_related_messages(self, message_uuid: str, get_previous: bool = False, only_uuids: bool = True) -> list[Message | str] | None:
        messages = []

        start_message: Message = await self.get_message(message_uuid)
        if start_message is None:
            return None

        history = await self.fetch_history()
        history_messages = history.messages

        if start_message.pos_in_history > 1:
            if start_message.is_alternative:
                for i in range(start_message.pos_in_history, 0, -1):
                    message = history_messages[i - 1]
                    if message.is_alternative:
                        messages.append(message)
                    else:
                        messages.append(message)
                        if get_previous and i > 1:
                            message = history_messages[i - 2]
                            messages.append(message)
                        break

            else:
                messages.append(start_message)

                if get_previous:
                    message = history_messages[start_message.pos_in_history - 2]
                    messages.append(message)
            messages.reverse()
        else:
            messages.append(start_message)

        if len(history_messages) > start_message.pos_in_history:
            for i in range(start_message.pos_in_history, len(history_messages)):
                message = history_messages[i]
                if message.is_alternative:
                    messages.append(message)
                else:
                    break

        if only_uuids:
            uuids = []
            for message in messages:
                uuids.append(message.uuid)
            return uuids
        else:
            return messages

    async def get_parent_message(self, message_uuid: str, only_uuid: bool = True ) -> Message | str | None:
        parent_message = None

        start_message: Message = await self.get_message(message_uuid)
        if start_message is None:
            return None

        if start_message.pos_in_history < 3:
            return None

        history = await self.fetch_history()
        history_messages = history.messages

        if start_message.is_alternative:
            for i in range(start_message.pos_in_history - 1, 0, -1):
                message = history_messages[i - 1]
                if not message.is_alternative and message.pos_in_history > 1:
                    parent_message = history_messages[i - 2]
                    break

        else:
            prev_message: Message = history_messages[start_message.pos_in_history - 2]
            if not prev_message.is_alternative:
                parent_message = prev_message

        if parent_message is None:
            return None

        if only_uuid:
            return parent_message.uuid
        else:
            return parent_message

    async def delete_messages(self, message_uuids: list) -> bool:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        if self.client.is_guest():
            raise Exception('Guest accounts cannot delete messages.')

        messages_to_delete = []

        try:
            for i in range(len(message_uuids)):
                message_uuid = message_uuids[i]

                if isinstance(message_uuid, str):
                    messages_to_delete.append(message_uuid)

        except:
            raise Exception("Failed to delete messages.")

        request = await self.requester.request('https://beta.character.ai/chat/history/msgs/delete/', options={
            "method": 'POST',
            "headers": self.client.get_headers(),
            "body": json.dumps({
                "history_id": self.history_id,
                "uuids_to_delete": messages_to_delete
            })
        })

        if request.status == 200:
            response = await request.json()

            if response.get('status', '') == 'OK':
                return True

        raise Exception('Failed to delete messages.')

    async def delete_message(self, message_uuid: str):
        await self.delete_messages([message_uuid])
