# Media types

---

### `Avatar` class
> representation of avatar. 

**methods**:


`get_file_name`
>```Python
>def get_file_name() -> str
>```
>
> **Description**:\
> *returns avatar file name (a.k.a. avatar_rel_path)*
> 
> **returns**: `str`


\
`get_url`
>```Python
>def get_url(size: int = 400, animated: bool = False) -> str
>```
>
> **Description**:\
> *returns link to the avatar image.*
> 
> **Params**:
> - size: (optional, default = `400`) `int` - *image size. Must be only 80, 200 or 400.*
> - animated: (optional, default = `False`) `bool` - *enables animation.*
>
> 
> **return type**: `TurnCandidate` | `None`

---

### `Voice` class
> representation of character voice.

**fields**: 
- **voice_id**: `str` - *Voice id.*
- **name**: `str` - *Voice name.*
- **description**: `str` - *Voice description.*
- **gender**: `str` - *Voice gender.*
- **visibility**: `str` - *Voice visibility (`public`, `unlisted` or `private`).*
- **preview_audio_url**: (optional) `str` - *Voice preview url.*
- **preview_text**: `str` - *Voice preview text.*
- **creator_id**: (optional) `str` - *Voice creator id.*
- **creator_username**: (optional) `str` - *Voice creator username.*
- **internal_status**: `str` - *Voice internal status.*
- **last_update_time**: (optional) `datetime` - *Voice last update time.*

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
    - [user](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/user.md)
    - [character](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/character.md)
    - [chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/chat.md)
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md)
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md) <- `(You're here.)`
