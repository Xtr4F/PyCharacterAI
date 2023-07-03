# Getting started

## Installation
First, you need to install the library:
```bash
pip install PyCharacterAI
```
> the library automatically downloads the chromium version you need for it to work



\
Then import the `Client` class from the library and create a new instance of it:
```Python
from PyCharacterAI import Client
```
```Python
client = Client()
```

\
Now you need to authenticate the `client`. This library allows you to authenticate in two ways.

1. As a guest:
```Python
await client.authenticate_as_guest()
```
> Some api features are not available

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

\
Now we get the `Chat`.
>To do this, you need to know the `character_id`. It is very easy to find it out:
>1. On the Character AI page, go to the chat with the character whose ID you want to find out
>2. Look at the page URL. Anything after `char=` is character ID:
>![img](https://i.ibb.co/TTt8x6B/image.png)
>
> > ![img](https://i.ibb.co/5nRQPLh/image.png)
> > 
> > ( if you switched to another chat  )

There are three ways to get a `chat` instance:

```Python
chat = await client.create_or_continue_chat('Character ID')
```
> Returns the last chat with character or creates a new one if there are no chats with that character.


```Python
chat = await client.create_chat('Character ID')
```
> Creates a new chat with character and returns it.


```Python
chat = await client.continue_chat('Character ID', 'History ID')
```
> Returns chat with character by its  `history_external_id`.

\
Now we can use the methods of the `Chat` class. Here is a simple example of code for chatting with character:
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

\
View the `Client` and `Chat` sections to get an idea of all available methods.

## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md) 
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md) <- `(You're here.)`
- API Reference:
  - [Client](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/client.md)
  - [Chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/chat.md)
  - Messages:
    - [Message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/messages/message.md)
    - [Reply](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/messages/reply.md)
    - [MessageHistory](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/messages/message_history.md)

