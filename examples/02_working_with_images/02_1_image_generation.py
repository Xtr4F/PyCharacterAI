import asyncio
from PyCharacterAI import Client

token = "TOKEN"


async def main():
    client = Client()
    await client.authenticate_with_token(token)

    username = (await client.fetch_user())['user']['username']
    print(f'Authenticated as {username}')

    while True:
        prompt = input("enter your prompt: ")

        url = await client.generate_image(prompt)
        print(f"Url of the generated image: {url}")


asyncio.run(main())