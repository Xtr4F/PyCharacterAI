# Account methods

---

### `fetch_me`
```Python
async def fetch_me() -> Account
```

**Description**:\
*fetches your account info*.

**Example**:
```Python
account = await client.account.fetch_me()

print(f"My name: {account.name}\n"
      f"My firstname: {account.first_name}\n"
      f"My username: {account.username}\n"
      f"My bio: {account.bio}")
```

**Returns** [Account](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md#Account-class)

---


### `fetch_my_settings`
```Python
async def fetch_my_settings() -> Dict
```

**Description**:\
*fetches your settings.* 

*Settings contains information about your*:
- ***default persona** (id of persona that is selected as default for all characters without a specified one)*
- ***persona overrides** (dictionary, where key is character id and value is persona id. If value is not empty, it means that you have set a specific persona for the character)*
- ***voice overrides** (dictionary, where key is character id and value is voice id. If value is not empty, it means that you have set a specific voice for the character*)

**Example**:
```Python
settings = await client.account.fetch_my_settings()

default_persona_id = settings.get("default_persona_id")
persona_overrides = settings.get("personaOverrides", {})
voice_overrides = settings.get("voiceOverrides", {})

print(f"My default_persona_id: {default_persona_id}")
print(f"\nPersona overrides for characters:")

for char_id, persona_id in persona_overrides.items():
    if persona_id:
        print(f"{char_id} -> {persona_id}")

print(f"\nVoice overrides for characters:")

for char_id, voice_id in voice_overrides.items():
    if voice_id:
        print(f"{char_id} -> {voice_id}")
```

**Returns** `Dict`

---


### `fetch_my_followers`
```Python
async def fetch_my_followers() -> List
```

**Description**:\
*fetches your followers.*

**Example**:
```Python
followers = await client.account.fetch_my_followers()

print("My followers:")

# I have no :(
for follower_username in followers:
    print(follower_username)
```

**Returns** `List[str]`

---



### `fetch_my_following`
```Python
async def fetch_my_following() -> List
```

**Description**:\
*fetches my following.*

**Example**:
```Python
following = await client.account.fetch_my_following()

print("I'm following:")

for following_username in following:
    print(following_username)
```

**Returns** `List[str]`

---


### `fetch_my_persona`
```Python
async def fetch_my_persona(persona_id: str) -> Persona
```

**Description**:\
*fetches information about your persona.*

**Params**:
- persona_id: `str` - *your persona id.*


**Returns** [Persona](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md#Persona-class)

---



### `fetch_my_personas`
```Python
async def fetch_my_personas() -> List[Persona]
```

**Description**:\
*fetches information about all your personas.*

**Example**:
```Python
my_personas = await client.account.fetch_my_personas()

print("My personas: ")

for persona in my_personas:
    print(f"Persona name: {persona.name}\n"
          f"Persona title: {persona.title}\n"
          f"Persona id: {persona.persona_id}\n")
```


**Returns** `List`[[Persona](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md#Persona-class)]

---



### `fetch_my_characters`
```Python
async def fetch_my_characters() -> List[CharacterShort]
```

**Description**:\
*fetches information about all the characters you've created.*

**Example**:
```Python
my_characters = await client.account.fetch_my_characters()

print("My characters: ")

for character in my_characters:
    print(f"Character name: {character.name}\n"
          f"Character title: {character.title}\n"
          f"Upvotes: {character.upvotes}\n"
          f"Interactions: {character.num_interactions}\n"
          f"Character visibility: {character.visibility}\n"
          f"Character id: {character.character_id}\n")
```

**Returns** `List`[[CharacterShort](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#CharacterShort-class)]

---



### `fetch_my_upvoted_characters`
```Python
async def fetch_my_upvoted_characters() -> List[CharacterShort]
```

**Description**:\
*fetches information about all the characters you've upvoted.*

**Returns** `List`[[CharacterShort](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#CharacterShort-class)]

---



### `fetch_my_voices`
```Python
async def fetch_my_voices() -> List[Voice]
```

**Description**:\
*fetches information about all the voices you've created.*

**Returns** `List`[[Voice](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md#Voice-class)]

---


### `edit_account`
```Python
async def edit_account(name: str, username: str, bio: str, avatar_rel_path: str) -> bool
```

**Description**:\
*edits your account.*

**Params**:
- name: `str` - ***new name** (must be at least 2 characters and no more than 50).*
- username: `str` - ***new username** (must be at least 2 characters and no more than 20).*
- bio: `str` - ***new bio** (must be no more than 500 characters).*
- avatar_rel_path: `str` - *avatar filename on c.ai server.*


**Returns** `bool`

---


### `create_persona`
```Python
async def create_persona(name: str, definition: str, avatar_rel_path: str) -> Persona
```

**Description**:\
*creates new persona.*

**Params**:
- name: `str` - ***persona name** (must be at least 3 characters and no more than 20).*
- definition: `str` - ***persona definition** (must be no more than 728 characters).*
- avatar_rel_path: `str` - *avatar filename on c.ai server.*


**Returns** [Persona](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md#Persona-class)

---



### `edit_persona`
```Python
async def edit_persona(persona_id: str, name: str, definition: str, avatar_rel_path: str) -> Persona
```

**Description**:\
*edits your persona.*

**Params**:
- persona_id: `str` - *id of persona you're trying to edit.*
- name: `str` - ***new persona name** (must be at least 3 characters and no more than 20).*
- definition: `str` - ***new persona definition** (must be no more than 728 characters).*
- avatar_rel_path: `str` - *avatar filename on c.ai server.*


**Returns** [Persona](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md#Persona-class)

---



### `delete_persona`
```Python
async def delete_persona(persona_id: str) -> bool
```

**Description**:\
*deletes your persona.*

**Params**:
- persona_id: `str` - *id of persona you're trying to delete.*


**Returns** `bool`

---



### `set_default_persona`
```Python
async def set_default_persona(persona_id: Union[str, None]) -> bool
```

**Description**:\
*sets persona as default for all characters you haven't specified a persona for.*

**Params**:
- persona_id: `str` or `None` - *id of persona you're trying to set as default. (pass `None` to unset current default persona.)*


**Returns** `bool`

---



### `unset_default_persona`
```Python
async def unset_default_persona() -> bool
```

**Description**:\
*unsets default persona.*

**Returns** `bool`

---



### `set_persona`
```Python
async def set_persona(character_id: str, persona_id: Union[str, None]) -> bool
```

**Description**:\
*sets persona for the character.*

**Params**:
- character_id: `str` - *id of the character you are trying to set a persona for.*
- persona_id: `str` or `None` - *id of persona  (pass `None` to unset persona for the character).*


**Returns** `bool`

---



### `unset_persona`
```Python
async def unset_persona(character_id: str) -> bool
```

**Description**:\
*unsets persona for the character.*

**Params**:
- character_id: `str` - *id of the character you are trying to unset a persona for.*


**Returns** `bool`

---



### `set_voice`
```Python
async def set_voice(character_id: str, voice_id: Union[str, None]) -> bool
```

**Description**:\
*sets voice for the character.*

**Params**:
- character_id: `str` - *id of the character you are trying to set a voice for.*
- voice_id: `str` or `None` - *id of voice  (pass `None` to unset voice for the character).*


**Returns** `bool`

---



### `unset_voice`
```Python
async def unset_voice(character_id: str) -> bool
```

**Description**:\
*unsets voice for the character.*

**Params**:
- character_id: `str` - *id of the character you are trying to unset a voice for.*


**Returns** `bool`

---



## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md)
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md)
- API Reference:
  - [methods](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods.md):
    - [account](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/account.md) <- `(You're here.)`
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
