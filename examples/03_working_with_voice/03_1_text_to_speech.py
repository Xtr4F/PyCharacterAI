import asyncio
from PyCharacterAI import Client

token = "Token"


async def main():
    client = Client()
    await client.authenticate_with_token(token)

    username = (await client.fetch_user())['user']['username']
    print(f'Authenticated as {username}')

    text = "Hi everybody! This is just a test of Text to speech feature Character AI. Bye bye !"
    voice = 22  # Anime Girl (F) (en-US)

    audio = await client.generate_voice(voice, text)

    filepath = "voice.mp3"  # Path to the directory where you want to save the audio
    with open(filepath, 'wb') as f:
        f.write(audio.read())


asyncio.run(main())