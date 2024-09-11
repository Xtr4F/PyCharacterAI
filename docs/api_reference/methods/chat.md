# Chat methods

---

### `fetch_histories`
```Python
async def fetch_histories(character_id: str, amount: int = 50) -> List[ChatHistory]:
```

**Description**:\
*fetches your histories (a.k.a. chat v1) with character.*


**Params**:
- character_id: `str` - *id of the character.*
- amount: (optional, default: `50`) `int` - *amount of histories to fetch.*


**Returns** `List[`[ChatHistory](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#ChatHistory-class)`]`

---

### `fetch_chats`
```Python
async def fetch_chats(character_id: str) -> List[Chat]:
```

**Description**:\
*fetches your chats with character.*


**Params**:
- character_id: `str` - *id of the character.*


**Returns** `List[`[Chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Chat-class)`]`

---


### `fetch_chat`
```Python
async def fetch_chat(chat_id: str) -> Chat
```

**Description**:\
*fetches information about your chat with character.*


**Params**:
- chat_id: `str` - *id of the chat you're trying to fetch.*


**Returns** [Chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Chat-class)

---




### `fetch_recent_chats`
```Python
async def fetch_recent_chats() -> List[Chat]:
```

**Description**:\
*fetches your recent chats with characters.*

**Example**:
```Python
chats = await client.chat.fetch_recent_chats()

print("I have recent chats with:")

for chat in chats:
    print(f"{chat.character_name} - [{chat.character_id}]")
```

**Returns** `List[`[Chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Chat-class)`]`

---

### `fetch_messages`
```Python
async def fetch_messages(chat_id, pinned_only: bool = False,
                         next_token: str = None) -> Tuple[List[Turn], Optional[str]]:
```

**Description**:\
*fetches messages in the chat with character.*

*Returns a tuple where the first element is list of messages and the second one is `next_token`. If `next_token` is not `None` it means that there are more messages, and they can be fetched by calling this method again, passing `next_token` as an argument.*


**Params**:
- chat_id: `str` - *id of the chat.*
- pinned_only: (optional, default: `False`) `bool` - *whether to fetch only the messages you have been pinned.*  
- next_token: (optional, default: `None`) `str` - *next token.*

**Example**:
```Python
next_token = None

while True:
    messages, next_token = await client.chat.fetch_messages(chatc, next_token=next_token)

    if not messages:
        break

    for message in messages:
        time = (f"{message.create_time.hour}:"
                f"{message.create_time.minute}:"
                f"{message.create_time.second}")

        print(f"({time}) [{message.author_name}]: "
                f"{message.get_primary_candidate().text}\n")

    if not next_token:
        break
```

**Returns** `Tuple[List[`[Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)`], Optional[str]]`

---

### `fetch_all_messages`
```Python
async def fetch_all_messages(chat_id, pinned_only: bool = False) -> List[Turn]:
```

**Description**:\
*fetches all the messages in the chat with character.*


**Params**:
- chat_id: `str` - *id of the chat.*
- pinned_only: (optional, default: `False`) `bool` - *whether to fetch only the messages you have been pinned.*

    
**Returns** `List[`[Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)`]`

---

### `fetch_pinned_messages`
```Python
async def fetch_pinned_messages(chat_id, next_token: str = None) -> [List[Turn], Optional[str]]:
```

**Description**:\
*fetches pinned messages in the chat with character.*

*Returns a tuple where the first element is list of pinned messages and the second one is `next_token`. If `next_token` is not `None` it means that there are more messages, and they can be fetched by calling this method again, passing `next_token` as an argument.*


**Params**:
- chat_id: `str` - *id of the chat.*
- next_token: (optional, default: `None`) `str` - *next token.*

**Returns** `Tuple[List[`[Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)`], Optional[str]]`

---

### `fetch_all_pinned_messages`
```Python
async def fetch_all_pinned_messages(chat_id: str) -> List[Turn]:
```

**Description**:\
*fetches all the pinned messages in the chat with character.*


**Params**:
- chat_id: `str` - *id of the chat.*

    
**Returns** `List[`[Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)`]`

---

### `fetch_following_messages`
```Python
async def fetch_following_messages(chat_id: str, turn_id: str, pinned_only: bool = False) -> List[Turn]:
```

**Description**:\
*fetches all the messages following a given message in the chat with character.*


**Params**:
- chat_id: `str` - *id of the chat.*
- turn_id: `str` - *id of the message relative to which you're trying to fetch the following ones.*
- pinned_only: (optional, default: `False`) `bool` - *whether to fetch only the messages you have been pinned.*

    
**Returns** `List[`[Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)`]`

---

### `update_chat_name`
```Python
async def update_chat_name(chat_id: str, name: str) -> bool
```

**Description**:\
*updates a name of the chat.*

**Params**:
- chat_id: `str` - *id of the chat.*
- name: `str` - *the name you're trying to give to the chat.*
    
**Returns** `bool`

---

### `archive_chat`
```Python
async def archive_chat(chat_id: str) -> bool
```

**Description**:\
*archives your chat.*

**Params**:
- chat_id: `str` - *id of the chat.*

**Returns** `bool`

---

### `unarchive_chat`
```Python
async def unarchive_chat(chat_id: str) -> bool
```

**Description**:\
*unarchives your chat.*

**Params**:
- chat_id: `str` - *id of the chat.*

**Returns** `bool`

---

### `copy_chat`
```Python
async def copy_chat(chat_id: str, end_turn_id: str) -> Union[str, None]
```

**Description**:\
*copies all the messages in the chat up to the `end_turn` to a new chat.*

*Returns id of the new chat.*

**Params**:
- chat_id: `str` - ***id of the chat.***
- end_turn_id: `str` - ***id of the message (turn) up to which the chat should be copied** ( if you want to copy the whole chat, pass id of the last message (turn) in the chat).*

**Returns** `str` | `None`

---

### `create_chat`
```Python
async def create_chat(character_id: str, greeting: bool = True) 
  -> Tuple[Chat, Optional[Turn]]:
```

**Description**:\
*creates a new chat with the character.*

*Returns a tuple where the first element is chat and the second one is greeting message. If you pass `greeting` as `False`, greeting message will be `None`.*


**Params**:
- character_id: `str` - *id of the character you're trying to create a chat with.*
- greeting: (optional, default: `True`) `bool` - *whether to generate a greeting message.*

**Example**:
```Python
character_id = "ID"

# I do want to have a greeting message.
chat, greeting_message = await client.chat.create_chat("character_id")
print(f"The new chat with id {chat.chat_id} created.")
print(greeting_message.get_primary_candidate().text)

# I do not want to have a greeting message.
chat, _ = await client.chat.create_chat("character_id", False)
print(f"The new chat with id {chat.chat_id} created.")
```

**Returns** `Tuple[`[Chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Chat-class), `Optional[`[Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)`]]`

---


### `update_primary_candidate`
```Python
async def update_primary_candidate(chat_id: str, turn_id, candidate_id: str) -> bool:
```

**Description**:\
*updates the primary candidate in turn (message).*

**Params**:
- chat_id: `str` - *id of the chat.*
- turn_id: `str` - *id of the message.*
- candidate_id: `str` - *id of the candidate you're trying to set as primary.*
    
**Returns** `bool`

---

### `send_message`
```Python
async def send_message(character_id: str, chat_id: str, text: str,
                       streaming: bool = False) -> Union[Turn, AsyncGenerator[Turn, Any]]:
```

**Description**:\
*sends a message to the chat with character.*

*Returns an answer message, or if you pass `streaming` as `True`, an async generator through which you can iterate to receive an answer message in parts, as is done on a website, instead of waiting for it to be completely generated.*


**Params**:
- character_id: `str` - *id of the character you're trying to send a message to.*
- chat_id: `str` - *id of the chat with character.*
- text: `str` - *your message text.*
- streaming: (optional, default = `False`) `bool`  - *whether to use streaming.*

**Example**:
```Python
# without streaming. 
while True:
    my_message = input("my message: ")

    answer = await client.chat.send_message("character_id", "chat_id", my_message)
    print(f"[{answer.author_name}]: {answer.get_primary_candidate().text}")
```
```Python    
# with streaming.
while True:
    my_message = input(f"my message: ")

    answer = await client.chat.send_message("character_id", "chat_id", my_message, streaming=True)

    printed_length = 0
    async for message in answer:
        if printed_length == 0:
            print(f"[{message.author_name}]: ", end="")

        text = message.get_primary_candidate().text
        print(text[printed_length:], end="")

        printed_length = len(text)
    print("\n")
```

**Returns** [Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)
 or`AsyncGenerator[`[Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)
,`Any]]`


---

### `another_response`
```Python
async def another_response(character_id: str, chat_id: str, turn_id: str,
                           streaming: bool = False) -> Union[Turn, AsyncGenerator[Turn, Any]]:
```

**Description**:\
*generates another response (turn candidate) from the character.*

*Returns an answer message with new turn candidate, or if you pass `streaming` as `True`, an async generator through which you can iterate to receive an answer message in parts, as is done on a website, instead of waiting for it to be completely generated.*


**Params**:
- character_id: `str` - *id of the character.*
- chat_id: `str` - *id of the chat with character.*
- turn_id: `str` - *id of the character message you are trying to generate an alternative response (candidate) for.*
- streaming: (optional, default = `False`) `bool`  - *whether to use streaming.*

**Example**:
```Python
# without streaming
answer = await client.chat.send_message("character_id", 
                                        "chat_id", 
                                        "message")

print(f"character response: \n{answer.get_primary_candidate().text}\n")

for counter in range(1, 4):
    # We're generating 3 alternative responses to our message.
    alternative_answer = await client.chat.another_response("character_id", 
                                                            "chat_id", 
                                                            answer.turn_id)

    print(f"alternative character response #{counter}: \n"
          f"{alternative_answer.get_primary_candidate().text}\n")
```
```Python
# with streaming
async def print_and_return_answer(answer):
    printed_length = 0
    answer_turn = None

    async for message in answer:
        text = message.get_primary_candidate().text
        print(text[printed_length:], end="")

        printed_length = len(text)

        answer_turn = message
    print("\n")

    return answer_turn

answer = await client.chat.send_message("character_id", 
                                        "chat_id", 
                                        "message", 
                                        streaming=True)

print(f"character response: \n")
answer = await print_and_return_answer(answer)

for counter in range(1, 4):
    # We're generating 3 alternative responses to our message.
    alternative_answer = await client.chat.another_response("character_id", 
                                                            "chat_id", 
                                                            answer.turn_id,
                                                            streaming=True)

    print(f"alternative character response #{counter}: \n")
    await print_and_return_answer(alternative_answer)
```

**Returns** [Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)
 or`AsyncGenerator[`[Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)
,`Any]]`


---

### `edit_message`
```Python
async def edit_message(chat_id: str, turn_id: str, candidate_id: str, text: str) -> Turn
```

**Description**:\
*edits message candidate text.*

*Returns turn with edited candidate.*

**Params**:
- chat_id: `str` - *id of the chat with character.*
- turn_id: `str` - *id of the message.*
- candidate_id: `str` - *id of the candidate you're trying to edit.*
- text: `str` - *new candidate text.*


**Returns** [Turn](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md#Turn-class)

---

### `delete_messages`
```Python
async def delete_messages(chat_id: str, turn_ids: [str]) -> bool:
```

**Description**:\
*deletes messages in the chat with character.*

**Params**:
- chat_id: `str` - *id of the chat.*
- turn_ids: `List[str]` - *ids of the messages you're trying to delete.*

**Returns** `bool`

---

### `delete_message`
```Python
async def delete_message(chat_id: str, turn_id: str) -> bool:
```

**Description**:\
*deletes a message in the chat with character.*

**Params**:
- chat_id: `str` - *id of the chat.*
- turn_id: `str` - *id of the message you're trying to delete.*

**Returns** `bool`

---
     

### `pin_message`
```Python
async def pin_message(chat_id: str, turn_id: str) -> bool:
```

**Description**:\
*pins a message in the chat with character.*

**Params**:
- chat_id: `str` - *id of the chat.*
- turn_id: `str` - *id of the message you're trying to pin.*

**Returns** `bool`

---
     
### `unpin_message`
```Python
async def unpin_message(chat_id: str, turn_id: str) -> bool:
```

**Description**:\
*unpins a message in the chat with character.*

**Params**:
- chat_id: `str` - *id of the chat.*
- turn_id: `str` - *id of the message you're trying to unpin.*

**Returns** `bool`

---


## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md)
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md)
- API Reference:
  - [methods](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods.md):
    - [account](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/account.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/chat.md) <- `(You're here.)`
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/user.md)
    - [utils](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/utils.md)
  - [types](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types.md):
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/chat.md)
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md)
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
