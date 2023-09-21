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
        print(f"{answer.src_character_name}: {answer.text}")  # Out: hello there! what kind of question you gonna ask me ? i'm here to assist you :)


asyncio.run(main())