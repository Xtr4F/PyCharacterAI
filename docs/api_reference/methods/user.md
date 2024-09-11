# User methods

---

### `fetch_user`
```Python
async def fetch_user(username: str) -> Union[PublicUser, None]:
```

**Description**:\
*fetches information about user by username.*


**Params**:
- username: `str` - *username of the user you are trying to fetch information about.*


**Returns** [PublicUser](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md#PublicUser-class) or `None`

---

### `fetch_user_voices`
```Python
async def fetch_user_voices(username: str) -> List[Voice]
```

**Description**:\
*fetches information about user's voices.*


**Params**:
- username: `str` - *username of the user whose voices you are trying to fetch.*


**Returns** `List[`[Voice](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md#Voice-class)`]` 

---

### `follow_user`
```Python
async def follow_user(username: str) -> bool:
```

**Description**:\
*follows you to the user.*


**Params**:
- username: `str` - *username of the user you are trying to follow.*


**Returns** `bool`

---
   

### `unfollow_user`
```Python
async def unfollow_user(username: str) -> bool:
```

**Description**:\
*unfollows you from the user.*


**Params**:
- username: `str` - *username of the user you are trying to unfollow from.*


**Returns** `bool`

---  


## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md)
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md)
- API Reference:
  - [methods](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods.md):
    - [account](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/account.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/chat.md)
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/user.md) <- `(You're here.)`
    - [utils](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/utils.md)
  - [types](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types.md):
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/chat.md)
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md)
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
