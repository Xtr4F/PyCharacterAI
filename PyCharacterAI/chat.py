import json

from PyCharacterAI.message import Message, MessageHistory, OutgoingMessage, Reply


class Chat:
    def __init__(self, client, character_id: str, continue_body: dict):
        self.chat_type = continue_body.get("type")

        self.character_id = character_id if not self.chat_type == "ROOM" else None
        self.history_id = continue_body.get('external_id')

        self.client = client

        ai = next(participant for participant in continue_body.get('participants') if not participant['is_human'])

        self.ai_id = ai['user']['username'] if not self.chat_type == "ROOM" else None
        self.requester = client.requester

    async def fetch_history(self, page_num: int = None, history_id: str = None) -> MessageHistory:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        page_string = f"&page_num={page_num}" if page_num else ""

        url = f"https://beta.character.ai/chat/history/msgs/user/?history_external_id={history_id if history_id else self.history_id}{page_string}"

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

    async def send_to_character(self, options: dict) -> Reply | None:
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
                if response.get("abort", False):
                    return Reply(chat=self, options=response)
                return None

            return messages.pop()
        raise Exception('Failed sending request to character.')

    async def send_message(self, text: str = "", primary_msg_uuid=None, image_path=None, image_description=None) -> Reply | None:
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

    async def rate_answer(self, rate: int, message_uuid: str, history_id: str = None) -> bool:
        r"""Rates the character's response
            :param history_id:
            :param message_uuid:
            :param rate: Number from 0 to 4 (number of stars)

            4 - Fantastic
            3 - Good
            2 - Bad
            1 - Terrible
            0 - Undo rate
        """
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        if rate > 4 or rate < 0:
            raise Exception('The rate should be between 1 and 4.')

        label_ids = [235, 238, 241, 244]

        match rate:
            case 4:
                label_ids = [235, 238, 241, 243]
            case 3:
                label_ids = [235, 238, 240, 244]
            case 2:
                label_ids = [235, 237, 241, 244]
            case 1:
                label_ids = [234, 238, 241, 244]
            case 0:
                label_ids = [235, 238, 241, 244]

        payload = {"message_uuid": message_uuid, "history_external_id": self.history_id if not history_id else history_id, "label_ids": label_ids, "admin_override": False}

        request = await self.requester.request("https://beta.character.ai/chat/annotations/label/", options={
            "method": "PUT",
            "headers": self.client.get_headers(),
            "body": json.dumps(payload)
        })

        if request.status == 200:
            return True
        return False

    async def get_message(self, message_uuid: str, history_id: str = None) -> Message | None:
        if not self.client.is_authenticated():
            raise Exception('You must be authenticated to do this.')

        history = await self.fetch_history(history_id)
        history_messages = history.messages

        for i in range(len(history_messages)):
            message = history_messages[i]

            if message.uuid == message_uuid:
                return message

        return None

    async def get_following_messages(self, message_uuid: str, history_id: str = None, only_uuids: bool = True) -> list[Message | str] | None:
        messages = []

        start_message: Message = await self.get_message(message_uuid, history_id)
        if start_message is None:
            return None

        history = await self.fetch_history(history_id)
        history_messages = history.messages

        if len(history_messages) > start_message.pos_in_history:
            for i in range(start_message.pos_in_history, len(history_messages) + 1):
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

    async def get_related_messages(self, message_uuid: str, history_id: str = None, get_previous: bool = False, only_uuids: bool = True) -> list[Message | str] | None:
        messages = []

        start_message: Message = await self.get_message(message_uuid, history_id)
        if start_message is None:
            return None

        history = await self.fetch_history(history_id)
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

    async def get_parent_message(self, message_uuid: str, history_id: str = None, only_uuid: bool = True) -> Message | str | None:
        parent_message = None

        start_message: Message = await self.get_message(message_uuid, history_id)
        if start_message is None:
            return None

        if start_message.pos_in_history < 3:
            return None

        history = await self.fetch_history(history_id)
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

    async def delete_messages(self, message_uuids: list, history_id: str = None) -> bool:
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
                "history_id": history_id if history_id else self.history_id,
                "uuids_to_delete": messages_to_delete
            })
        })

        if request.status == 200:
            response = await request.json()

            if response.get('status', '') == 'OK':
                return True

        raise Exception('Failed to delete messages.')

    async def delete_message(self, message_uuid: str, history_id: str = None):
        await self.delete_messages([message_uuid], history_id)
