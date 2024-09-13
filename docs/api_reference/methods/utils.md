# Utils methods

---

### `ping`
```Python
async def ping() -> bool:
```

**Description**:\
*sends a ping request.*

**Returns** `bool`

---

### `fetch_voice`
```Python
async def fetch_voice(voice_id: str) -> Voice:
```

**Description**:\
*fetches a voice by given voice id.*

**Params**:
- voice_id: `str` - *id of the voice.*

**Returns**  [Voice](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md#Voice-class)

---


### `search_voices`
```Python
async def search_voices(voice_name: str) -> List[Voice]:
```

**Description**:\
*searches for voices by given name.*


**Params**:
- voice_name: `str` - *name of the voice.*


**Example**:
```Python
voice_name = "girl"
voices = await client.utils.search_voices(voice_name)

print(f"search results for {voice_name}: ")

for voice in voices:
    print(f"{voice.name} [{voice.voice_id}]")
```

**Returns** `List[`[Voice](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md#Voice-class)`]`

---

### `generate_image`
```Python
async def generate_image(prompt: str) -> List[str]:
```

**Description**:\
*generates the images for given prompt.*

*Returns a list of links to generated images.*

**Params**:
- prompt: `str` - *your prompt.*

**Example**:
```Python
prompt = "moon and sea"

images = await client.utils.generate_image(prompt)

print(f"generated images by the prompt \"{prompt}\": ")

for image_url in images:
    print(image_url)
```


**Returns** `List[str]`

---

### `upload_avatar`
```Python
async def upload_avatar(image: str, check_image: bool = True) -> Avatar:
```

**Description**:\
*uploads your image to use it as an avatar for character/persona/profile.*

***NOTE: This method requires the specified web_next_auth token***


**Params**:
- image: `str` - *filepath or url.*
- check_image: (optional, default: `True`) `bool` - *whether to check the validity of the uploaded avatar (makes one more additional request).*

**Example**:
```Python
avatar_file = "path to file or url"

avatar = await client.utils.upload_avatar(avatar_file)

print(f"avatar uploaded successfully. Url: {avatar.get_url()}\n")

# You can use this as an avatar_rel_path
filename = avatar.get_file_name()
print(f"avatar rel path: {filename}")
```


**Returns**  [Avatar](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md#Avatar-class)


---

### `upload_voice`
```Python
async def upload_voice(voice: str, name: str, description: str = "", visibility: str = "private") -> Voice:
```

**Description**:\
*uploads your audio as a voice for characters.*

**Params**:
- voice: `str` - ***filepath or url.***
- name: `str` - ***voice name** (must be at least 3 characters and no more than 20).*
- description: (optional) `str` - ***voice description** (must be no more than 120 characters).*
- visibility: (optional, default: `"private"`) `str` - ***voice visibility** (`public` or `private`).* 

**Example**:
```Python
voice_file = "path to file or url"
voice = await client.utils.upload_voice(voice_file, "voice name", "voice description")

print(f"voice uploaded successfully.\n"
      f"voice_id: {voice.voice_id}\n"
      f"preview: {voice.preview_audio_url}")
```

**Returns**  [Voice](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md#Voice-class)


---

### `edit_voice`
```Python
async def edit_voice(voice: Union[str, Voice], name: str = None, description: str = None, visibility: str = None) -> Voice:
```

**Description**:\
*edits your voice.*

**Params**:
- voice: `str` or `Voice` - ***id of the voice you're trying to edit or Voice object.***
- name: (optional) `str` - ***new voice name** (must be at least 3 characters and no more than 20).*
- description: (optional) `str` - ***new voice description** (must be no more than 120 characters).*
- visibility: (optional) `str` - ***new voice visibility** (`public` or `private`).* 


**Returns**  [Voice](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md#Voice-class)


---

### `delete_voice`
```Python
async def delete_voice(voice_id: str) -> bool:
```

**Description**:\
*deletes your voice.*

**Params**:
- voice_id: `str` - ***id of the voice you're trying to delete.***


**Returns** `bool`

---

### `generate_speech`
```Python
async def generate_speech(chat_id: str, turn_id: str, candidate_id: str, voice_id: str, 
                          **kwargs) -> Union[bytes, str]:
```

**Description**:\
*generate speech from the character's message candidate.*

**Params**:
- chat_id: `str` - *id of the chat.*
- turn_id: `str` - *id of the message (turn).*
- candidate_id: `str` - *id of the message candidate.*
- voice_id: `str` - *id of the voice.*

**Additional params (kwargs)**:
- return_url: (optional, default: `False`) - *If you pass `True`, the method will return the url to the generated speech instead of making an additional request to get the `bytes`.* 


**Example**:
```Python
speech = await client.utils.generate_speech("chat_id", "turn_id", "candidate_id", 
                                            "voice_id")

filepath = "voice.mp3"

with open(filepath, 'wb') as f:
     f.write(speech)
```
```Python
# or you can get just the url.
speech_url = await client.utils.generate_speech("chat_id", "turn_id", "candidate_id", 
                                            "voice_id", return_url=True)

```

**Returns**  `bytes` or `str`

---
  
       
    

## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md)
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md)
- API Reference:
  - [methods](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods.md):
    - [account](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/account.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/chat.md)
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/user.md)
    - [utils](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/utils.md) <- `(You're here.)`
  - [types](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types.md):
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/chat.md)
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md)
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
