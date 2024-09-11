# Character methods

---


### `fetch_characters_by_category`
```Python
async def fetch_characters_by_category() -> Dict[str, List[CharacterShort]]:
```

**Description**:\
*fetches characters by categories.*

*Returns dict, where key is category and value is list of characters related to this category.*

**Example**:
```Python
characters = await client.character.fetch_characters_by_category()

for category in characters:
    print(f"\n{category}: ")

    for character in characters[category]:
        print(f"{character.name} [{character.character_id}]")
```


**Returns** `Dict[str, List[`[CharacterShort](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#CharacterShort-class)`]]`

---

### `fetch_recommended_characters`
```Python
async def fetch_recommended_characters() -> List[CharacterShort]:
```

**Description**:\
*fetches recommended characters.*


**Returns** `List[`[CharacterShort](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#CharacterShort-class)`]`

---

### `fetch_featured_characters`
```Python
async def fetch_featured_characters() -> List[CharacterShort]:
```

**Description**:\
*fetches featured characters.*


**Returns** `List[`[CharacterShort](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#CharacterShort-class)`]`

---

### `fetch_similar_characters`
```Python
async def fetch_similar_characters(character_id: str) -> List[CharacterShort]:
```

**Description**:\
*fetches similar characters.*


**Params**:
- character_id: `str` - *id of the character.*


**Returns** `List[`[CharacterShort](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#CharacterShort-class)`]`

---

### `fetch_character_info`
```Python
async def fetch_character_info(character_id: str) -> Character:
```

**Description**:\
*fetches information about character.*


**Params**:
- character_id: `str` - *id of the character.*


**Returns** [Character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#Character-class)

---

### `search_characters`
```Python
async def search_characters(character_name: str) -> List[CharacterShort]:
```

**Description**:\
*searches for characters.*


**Params**:
- character_name: `str` - *name of the character.*

**Example**:
```Python
name = "Catgirl"  # Why not.
characters = await client.character.search_characters(name)  

print(f"Search results for {name}:")

for character in characters:
    print(f"Name: {character.name}. Id: {character.character_id}")
```

**Returns** `List[`[CharacterShort](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#CharacterShort-class)`]`

---

### `search_creators`
```Python
async def search_creators(creator_name: str) -> List[str]:
```

**Description**:\
*searches for creators.*

*Returns list of creator usernames.*


**Params**:
- creator_name: `str` - *name of the creator.*


**Returns** `List[str]`

---

### `character_vote`
```Python
async def character_vote(character_id: str, vote: Union[bool, None]) -> bool:
```

**Description**:\
*votes for character (likes or dislikes).*


**Params**:
- character_id: `str` - *id of the character you're trying to vote for.*
- vote: `bool` or `None` - ***your vote** (pass `True` to like, `False` to dislike, and `None` to remove the vote).*


**Returns** `bool`

---

### `create_character`
```Python
async def create_character(name: str, greeting: str, title: str = "", description: str = "",
                           definition: str = "", copyable: bool = False, visibility: str = "PRIVATE",
                           avatar_rel_path: str = "", default_voice_id: str = "") -> Character:
```

**Description**:\
*creates new character.*


**Params**:
- name: `str` - ***character name** (must be at least 3 characters and no more than 20).*


- greeting: `str` - ***character greeting** (must be at least 3 characters and no more than 2048).*


- title: `str` (optional) - ***character title** (must be at least 3 characters and no more than 50).*   


- description: `str` (optional) - ***character description** (must be no more than 500 characters).*  


- definition: `str` (optional) - ***character definition** (must be no more than 32000 characters).*   


- copyable: `bool` (optional, default: `False`) - ***whether the character can be copied. In other words, whether its definition is visible.***


- visibility: `str` (optional, default: `"private"`) - ***character visibility** (`public`, `unlisted` or `private`).*   


- avatar_rel_path: `str` (optional) - ***avatar filename on c.ai server.*** 


- default_voice_id: `str` (optional) - ***id of the voice that will be the default character voice.***


**Returns** [Character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#Character-class)

---

### `edit_character`
```Python
async def edit_character(character_id: str, name: str, greeting: str, title: str = "", description: str = "",
                         definition: str = "", copyable: bool = False, visibility: str = "private",
                         avatar_rel_path: str = "", default_voice_id: str = "") -> Character
```

**Description**:\
*edits your character.*


**Params**:
- character_id: `str` - ***id of the character you're trying to edit.***


- name: `str` - ***character name** (must be at least 3 characters and no more than 20).*


- greeting: `str` - ***character greeting** (must be at least 3 characters and no more than 2048).*


- title: `str` (optional) - ***character title** (must be at least 3 characters and no more than 50).*   


- description: `str` (optional) - ***character description** (must be no more than 500 characters).*  


- definition: `str` (optional) - ***character definition** (must be no more than 32000 characters).*   


- copyable: `bool` (optional, default: `False`) - ***whether the character can be copied. In other words, whether its definition is visible.***


- visibility: `str` (optional, default: `"private"`) - ***character visibility** (`public`, `unlisted` or `private`).*   


- avatar_rel_path: `str` (optional) - ***avatar filename on c.ai server.*** 


- default_voice_id: `str` (optional) - ***id of the voice that will be the default character voice.***


**Returns** [Character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md#Character-class)

---
 



## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md)
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md)
- API Reference:
  - [methods](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods.md):
    - [account](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/account.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/character.md) <- `(You're here.)`
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/chat.md)
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/user.md)
    - [utils](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/utils.md)
  - [types](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types.md):
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/chat.md)
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md)
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
