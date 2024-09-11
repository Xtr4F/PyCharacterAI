import asyncio
from PyCharacterAI import Client

token = "TOKEN"
character_id = "ID"


async def main():
    client = Client()
    await client.authenticate(token)

    me = await client.account.fetch_me()
    print(f'Authenticated as @{me.username}')

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