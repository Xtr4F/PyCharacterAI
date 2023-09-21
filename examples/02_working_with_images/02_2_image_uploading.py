import asyncio
from PyCharacterAI import Client

token = "TOKEN"

image = "https://i.ibb.co/RcF8K7S/image.jpg"  # URL or path to the image


async def main():
    client = Client()
    await client.authenticate_with_token(token)

    username = (await client.fetch_user())['user']['username']
    print(f'Authenticated as {username}')

    image_url = (await client.upload_image(image))['response']

    # Use the given URL to attach an image to the message

    character_id = "zb7I4U9OYfewmEgOWLBHScefPeELkm1J-_GZDjHLY1M"  # Ask me anything (by @harmlessharvest)

    chat = await client.create_or_continue_chat(character_id)

    answer = await chat.send_message("Look at that beautiful sunset ! ", image_path=image_url)
    print(answer.text)


asyncio.run(main())