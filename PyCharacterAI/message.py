class OutgoingMessage:
    def __init__(self, chat, options: dict):
        payload = {
            "history_external_id": options.get("history_external_id", chat.history_id),
            "character_external_id": options.get("character_external_id", chat.character_id),
            "text": options.get("text", ""),
            "tgt": options.get("tgt", chat.ai_id),
            "ranking_method": options.get("ranking_method", 'random'),
            "faux_chat": options.get("faux_chat", False),
            "staging": options.get("staging", False),
            "model_server_address": options.get("model_server_address", None),
            "override_prefix": options.get("override_prefix", None),
            "override_rank": options.get("override_rank", None),
            "rank_candidates": options.get("rank_candidates", None),
            "filter_candidates": options.get("filter_candidates", None),
            "prefix_limit": options.get("prefix_limit", None),
            "prefix_token_limit": options.get("prefix_token_limit", None),
            "livetune_coeff": options.get("livetune_coeff", None),
            "parent_msg_uuid": options.get("parent_msg_uuid", None),
            "stream_params": options.get("stream_params", None),
            "enable_tti": options.get("initial_timeout", True),
            "initial_timeout": options.get("initial_timeout", None),
            "insert_beginning": options.get("insert_beginning", None),
            "translate_candidates": options.get("translate_candidates", None),
            "stream_every_n_steps": options.get("stream_every_n_steps", 16),
            "chunks_to_pad": options.get("chunks_to_pad", 8),
            "is_proactive": options.get("is_proactive", False),
            "give_room_introductions": options.get("give_room_introductions", True),

            "image_rel_path": options.get("image_rel_path", ""),
            "image_description": options.get("image_description", ""),
            "image_description_type": options.get("image_description_type", "AUTO_IMAGE_CAPTIONING"),
            "image_origin_type": options.get("image_origin_type", "UPLOADED")
        }

        if not options.get("primary_msg_uuid", None) is None:
            payload['primary_msg_uuid'] = options.get("primary_msg_uuid", None)
            payload['seen_msg_uuids'] = [options.get("primary_msg_uuid", None)]

        if not options.get("unsanitized_characters", None) is None:
            payload["unsanitized_characters"] = options.get("unsanitized_characters", None)

        self.payload = payload

    def get_payload(self):
        return self.payload


class Message:
    def __init__(self, chat, options):
        self.chat = chat
        self.raw_options = options

        self.uuid = options.get("uuid", None)
        self.id = options.get("id", None)
        self.text = options.get("text", None)
        self.src = options.get("src", None)
        self.tgt = options.get("tgt", None)
        self.pos_in_history = options.get("pos_in_history", None)
        self.is_alternative = options.get("is_alternative", None)
        self.image_relative_path = options.get("image_rel_path", None)
        self.image_prompt_text = options.get("image_prompt_text", None)
        self.deleted = None
        self.src_name = options.get("src__name", None)
        self.src_internal_id = options.get("src__user__username", None)
        self.src_is_human = options.get("src__is_human", None)
        self.src_character_avatar_file_name = options.get("src__character__avatar_file_name", None)
        self.src_character_dict = options.get("src_char", None)
        self.responsible_username = options.get("responsible_user__username", None)


class Reply:
    def __init__(self, chat, options: dict):
        if options.get("force_login", False):
            raise Exception("Too many messages! (this might be because you use a guest account)")

        self.chat = chat

        self.is_aborted = options.get('abort', False)

        reply_options = options.get('replies', [{}])[0]
        self.text = reply_options.get('text', None)
        self.id = reply_options.get('id', None)
        self.uuid = reply_options.get('uuid', None)

        self.image_relative_path = reply_options.get('image_rel_path', None)

        src_char_dict = options.get('src_char', {})
        self.src_character_name = src_char_dict.get('participant', {}).get('name', None)
        self.src_avatar_file_name = src_char_dict.get('avatar_file_name', None)

        self.is_final_chunk = options.get('is_final_chunk', False) if not self.is_aborted else False
        self.last_user_message_id = options.get('last_user_msg_id', None)
        self.last_user_msg_uuid = options.get('last_user_msg_uuid', None)

    async def get_message(self):
        return await self.chat.get_message(self.uuid)

    async def rate(self, rate: int):
        return await self.chat.rate_answer(rate, self.uuid)


class MessageHistory:
    def __init__(self, chat, messages, has_more, next_page):
        self.chat = chat
        self.messages = messages
        self.hasMore = has_more
        self.nextPage = next_page
