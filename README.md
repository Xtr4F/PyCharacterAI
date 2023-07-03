# PyCharacterAI
> An unofficial asynchronous api wrapper for [Character AI](https://character.ai/). For Python.
##

This library is based on the [Character AI Unofficial Node API](https://github.com/realcoloride/node_characterai), made by [realcoloride](https://github.com/realcoloride). 

If you have any questions, problems, suggestions, please contact me:

[![Tag](https://img.shields.io/badge/discord-server-black?style=flat&logo=Discord)](https://discord.gg/MN7pMbH2)
[![Tag](https://img.shields.io/badge/telegram-dm-black?style=flat&logo=Telegram)](https://t.me/XtraF)
## Installation
```bash
pip install PyCharacterAI
```


## Getting started
> First, import and create a new instance of the Client class
```Python
from PyCharacterAI import Client
```
```Python
client = Client()
```

This library allows you to authenticate in two ways:

1. As a guest (Some api features are not available):
```Python
await client.authenticate_as_guest()
```

2. Using a token:
```Python
token = 'TOKEN'
await client.authenticate_with_token(token)
```
> Instructions for getting a token:
> 
> 1. Open the Character AI website in your browser
> 2. Open the developer tools `F12` and go to the `Application` tab.
> 3. Go to the `Storage` section and click on `Local Storage`.
> 4. Look for the `@@auth0spajs@@::dyD3gE281MqgISG7FuIXYhL2WEknqZzv::https://auth0.character.ai/::openid profile email offline_access` key.
> 5. Open the body and copy the access token.

> ![Access_Token](https://i.imgur.com/09Q9mLe.png)
>
> ⚠️ Warning! Do not share this token with anyone!


## Simple example

```Python
import asyncio
from PyCharacterAI import Client

token = "TOKEN"


async def main():
    client = Client()
    await client.authenticate_with_token(token)

    username = (await client.fetch_user())['user']['username']
    print(f'Authenticated as {username}')

    character_id = "iV5qb8ttzD7Ytl69U_-ONcW2tW_lrFrOVKExyKJHlJM"  # Lily (by @landon)
    chat = await client.create_or_continue_chat(character_id)

    while True:
        message = input(f'{username}: ')  # In: Hi!

        answer = await chat.send_message(message)
        print(f"Character: {answer.text}")  # Out: hello there! what kind of question you gonna ask me ? i'm here to assist you :)


asyncio.run(main())
```

## Documentation
The library has [documentation](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md).
