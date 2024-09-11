# Chat types

---

### `Chat` class
> representation of chat (a.k.a. chat v2)

fields: 
- **chat_id**: `str` - *Chat id.*
- **character_id**: `str` - *Character id.*
- **creator_id**: `str` - *Chat creator id.*
- **create_time**: (optional) `datetime` - *Chat creation time.*
- **state**: `str` - *Chat state.*
- **chat_type**: `str` - *Chat type.*
- **chat_name: `str` - *Chat name (will be `None` if you didn't specify it.).*
- **visibility**: `str` - *Chat visibility (`public`, `unlisted` or `private`).*
- **preview_turns**: `list[Turn]` - *Preview of last chat messages.*
---
These fields are not `None` only when calling `.fetch_recent_chats()`:
- **character_name**: (optional) `str` - *Character name.*
- **character_avatar**: (optional) `Avatar` - *Character avatar.*
---

### `ChatHistory` class
> representation of history (a.k.a. chat v1)
> 
> only for the sake of it. Use chat v2 instead.

fields: 
- **chat_id**: `str` - *History id.*
- **create_time**: (optional) `datetime` - *History creation time.*
- **last_interaction**: `datetime` - *Last interaction time.*
- **preview_messages**: `list[HistoryMessage]` - *Preview of last chat messages.*

---

## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md)
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md)
- API Reference:
  - [methods](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods.md):
    - [account](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/account.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/chat.md)
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/user.md)
    - [utils](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/utils.md)
  - [types](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types.md):
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/chat.md) <- `(You're here.)`
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md)
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
