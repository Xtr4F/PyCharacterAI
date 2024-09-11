# Character types

---

### `CharacterShort` class
> short information about character

fields: 
- **character_id**: `str` - *Character id.* 
- **title**: `str` - *Character title.* 
- **name**: `str` - *Character name.*
- **visibility**: `str` - *Character visibility (`public`, `unlisted` or `private`).*
- **greeting**: `str` - *Character greeting.*
- **description**: `str` - *Character description.* 
- **definition**: `str` - *Character definition.*
- **upvotes**: (optional) `int` - *Character's number of likes.* 
- **author_username** : (optional) `str` - *Character creator username.*
- **num_interactions**: (optional) `int` - *Number of interactions with character.* 
- **avatar**: (optional) `Avatar` - *Character avatar.* 

---

### `Character` class
> full information about character

fields: 
- **character_id**: `str` - *Character id.* 
- **title**: `str` - *Character title.* 
- **name**: `str` - *Character name.*
- **visibility**: `str` - *Character visibility (`public`, `unlisted` or `private`).*
- **greeting**: `str` - *Character greeting.*
- **description**: `str` - *Character description.* 
- **definition**: `str` - *Character definition.*
- **upvotes**: (optional) `int` - *Character's number of likes.* 
- **author_username** : (optional) `str` - *Character creator username.*
- **num_interactions**: (optional) `int` - *Number of interactions with character.* 
- **avatar**: (optional) `Avatar` - *Character avatar.* 
---
- **copyable**: `bool` - *Whether the character can be copied. In other words, whether its definition is visible.*
- **identifier**: `str` - Character identifier.
- **img_gen_enabled**: `bool` - *Whether the character can generate images.*
- **base_img_prompt**: `str` - *Basic prompt for generating images.*
- **img_prompt_regex**: `str` - *Regex for image prompt.*
- **strip_img_prompt_from_msg**: `bool` - *Whether the prompt is removed from the message.*
- **starter_prompts**: `dict` - *Prompts to start a chat with.*
- **comments_enabled**: `bool` - *IDK.*
- **internal_id**: `str` - *Character internal id.*
- **voice_id**: `str` - *Character voice id.*
- **default_voice_id**: `str` - *Character default voice id.*
- **songs**: `list` - *List of character songs, probably. IDK.*




## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md)
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md)
- API Reference:
  - [methods](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods.md):
    - [account](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/account.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/chat.md)
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/user.md)
    - [utils](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/utils.md)
  - [types](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types.md):
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md) <- `(You're here.)`
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/chat.md)
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md)
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
