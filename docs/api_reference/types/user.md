# User types

---


### `Account` class
> representation of your account.

fields:

- **username**: `str` - *Your account username.*
- **name**: `str` - *Your account name.*
- **bio**: `str` - *Your account bio.*
- **avatar**: (optional) `Avatar` - *Your account avatar.*
---
- **account_id**: `str` - *Your account id.*
- **first_name**: (optional) `str` - *Your firstname.*
- **avatar_type**: `str` - *avatar type: (DEFAULT or UPLOADED)*
- **is_human**: `bool` - *Whether the account is human.*
- **email**: (optional) `str` - *Your email.*
---

### `PublicUser` class
> representation of user.

fields:
- **username**: `str` - *User username.*
- **name**: `str` - *User name.*
- **bio**: `str` - *User bio.*
- **avatar**: (optional) `Avatar` - *User avatar.*
---
- **num_following**: `int` - *Number of following.*
- **num_followers**: `int` - *Number of followers.*
- **characters**: `list[CharacterShort]` - *List of user's public characters.*
- **subscription_type**: `str` - *User's subscription type.*

---

### `Persona` class
> representation of persona.

fields:
- **persona_id**: `str` - *Persona id.*
- **name**: `str` - *Persona name.*
- **definition**: `str` - *Persona definition.*
- **avatar**: (optional) `Avatar` - *Persona avatar.*
- **author_username**: (optional) `str` - *Persona creator username.*

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
    - [utils](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/utils.md)
  - [types](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types.md):
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md) <- `(You're here.)`
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/chat.md)
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md)
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
