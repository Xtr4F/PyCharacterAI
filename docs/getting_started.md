## Getting started


First, you need to install the library:
```bash
pip install git+https://github.com/Xtr4F/PyCharacterAI
```


\
Import the `Client` class from the library and create a new instance of it:
```Python
from PyCharacterAI import Client
```

```Python
client = Client()
```

Then you need to authenticate `client` using `token`:
```Python
await client.authenticate("TOKEN")
```

> if you want to be able to upload your avatar you also need to specify `web_next_auth` token as an additional argument (only this way for now, this may change in the future):
> ```Python
> await client.authenticate("TOKEN", web_next_auth="WEB_NEXT_AUTH")
> ```
After authentication, we can use all available library methods.

---
## About tokens and how to get them:
> ⚠️ WARNING, DO NOT SHARE THESE TOKENS WITH ANYONE! Anyone with your tokens has full access to your account! 

This library uses two types of tokens: a common `token` and `web_next_auth`. The first one is required for almost all methods here and the second one only and only for `upload_avatar()` method (may change in the future).

### Instructions for getting a `token`:
1. Open the Character.AI website in your browser
2. Open the `developer tools` (`F12`, `Ctrl+Shift+I`, or `Cmd+J`)
3. Go to the `Nerwork` tab
4. Interact with website in some way, for example, go to your profile and look for `Authorization` in the request header
5. Copy the value after `Token`
> For example, token in `https://plus.character.ai/chat/user/public/following/` request headers:
> ![img](https://github.com/Xtr4F/PyCharacterAI/blob/main/assets/token.png)

### Instructions for getting a `web_next_auth` token:
1. Open the Character.AI website in your browser
2. Open the `developer tools` (`F12`, `Ctrl+Shift+I`, or `Cmd+J`)
3. Go to the `Storage` section and click on `Cookies`
4. Look for the `web-next-auth` key
5. Copy its value
> ![img](https://github.com/Xtr4F/PyCharacterAI/blob/main/assets/web_next_auth.png)

---

## Some important concepts

> Further, in the documentation you can find  certain concepts, some of them I want to explain below. Some concepts related to character creation and user personas can be found in the official [character book](https://book.character.ai/character-book/).

### turn and candidate

**Turn** *is a message in chat. It contains one or more `candidates` that represent the content of this message. Just keep in mind that `turn` == `message`.*

**Candidate** (or **TurnCandidate**) *is the "content" of the message (`turn`). A message can have several `candidates` (for example, when you swipe the character's answer on the c.ai website, you create new `candidate` for the character's message).* 

**Primary candidate** - *currently selected `candidate`. When you send a new message to the chat, you reply to this (primary) `message candidate`. When a new alternative response is generated, `primary candidate` automatically updates to the newly generated `candidate`. You can also manually set a specific `turn candidate` as a primary if you want to reply to a particular `message candidate`. (Refer to the documentation for more details.)*

\
...to be completed

---
## Examples
> Here are just some examples of the library's features. If you want to know about all `methods` and `types` with explanations, go to [methods](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods.md) and [types](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types.md) documentation sections.
### Simple chatting example:
```Python
import asyncio
from PyCharacterAI import Client

token = "TOKEN"
character_id = "ID"


async def main():
    client = Client()
    await client.authenticate(token)

    me = await client.account.fetch_me()
    print(f"Authenticated as @{me.username}")

    chat, greeting_message = await client.chat.create_chat(character_id)

    print(f"{greeting_message.author_name}: {greeting_message.get_primary_candidate().text}")

    while True:
        message = input(f"[{me.name}]: ")

        answer = await client.chat.send_message(character_id, chat.chat_id, message)
        print(f"[{answer.author_name}]: {answer.get_primary_candidate().text}")

asyncio.run(main())
```
---
A more advanced example. You can use so-called streaming to receive a message in parts, as is done on a website, instead of waiting for it to be completely generated:
```Python
import asyncio
from PyCharacterAI import Client

token = "TOKEN"
character_id = "ID"


async def main():
    client = Client()
    await client.authenticate(token)

    me = await client.account.fetch_me()
    print(f"Authenticated as @{me.username}")

    chat, greeting_message = await client.chat.create_chat(character_id)

    print(f"[{greeting_message.author_name}]: {greeting_message.get_primary_candidate().text}")

    while True:
        message = input(f"[{me.name}]: ")

        answer = await client.chat.send_message(character_id, chat.chat_id, message, streaming=True)

        printed_length = 0
        async for message in answer:
            if printed_length == 0:
                print(f"[{message.author_name}]: ", end="")

            text = message.get_primary_candidate().text
            print(text[printed_length:], end="")

            printed_length = len(text)
        print("\n")


asyncio.run(main())
```
---
### Working with images:
```Python
# We can generate images by a prompt
# (It will return list of urls)
images = await client.utils.generate_image("prompt")
```
```Python
# We can upload an image to use it as an 
# avatar for character/persona/profile

# NOTE: This method requires the specified web_next_auth token
avatar_file = "path to file or url"
avatar = await client.utils.upload_avatar(avatar_file)
```

---
### Working with voices:
```Python
# We can search for voices
voices = await client.utils.search_voices("name")
```

```Python
# We can upload the audio as a voice
voice_file = "path to file or url"
voice = await client.utils.upload_voice(voice_file, "voice name")
```

```Python
# We can set and unset a voice for character  
await client.account.set_voice("character_id", "voice_id")
await client.account.unset_voice("character_id")
```

```Python
# And we can use voice to generate speech from the character's messages
speech = await client.utils.generate_speech("chat_id", "turn_id", "candidate_id", "voice_id")
```
> ```Python
> # It will return bytes, so we can use it for example like this:
> filepath = "voice.mp3"
>
> with open(filepath, 'wb') as f:
>    f.write(speech)
> ```

---

## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md) 
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md) <- `(You're here.)`
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
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/chat.md)
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md)
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
