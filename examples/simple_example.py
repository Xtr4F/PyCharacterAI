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