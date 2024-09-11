# Message types

---

### `HistoryMessage` class
> representation of message in history (a.k.a. chat v1)
> 
> only for the sake of it. Use chat v2 instead.

fields: 
- **uuid**: `str` - *Message uuid.*
- **id**: `str` - *Message id.*
- **text**: `str` - *Message text.*
- **src**: `dict` - *src. IDK*
- **tgt**: `dict` - *tgt. IDK*
- **is_alternative**: `bool` - *Whether the message is alternative.*
- **image_relative_path**: = `str` - *image relative path.*

---

### `Turn` class
> representation of message in chat (a.k.a. chat v2)

fields:
- **chat_id**: `str` - *Chat id.*
- **turn_id**: `str`- *Turn id.*

- **create_time**: (optional) `datetime` - *Turn creation time.*
- **last_update_time**: (optional) `datetime` = *Turn last update time.*

- **state**: `str` - *Turn state.*

- **author_id**: `str` - *Turn author id.*
- **author_name**: `str` - *Turn author name.*
- **author_is_human**: `bool` - *Whether the turn author is human.*

- **candidates**: `{str: TurnCandidate}` - *Dict with all the turn candidates. Where: key is candidate id and value is `TurnCandidate` object.*

- **primary_candidate_id**: (optional) `str` - *Primary candidate id.*

\
**methods**:\
\
`get_candidates`
>```Python
>def get_candidates() -> [TurnCandidate]
>```
>
> **Description**:\
> *returns list with all the turn candidates.*
> 
> 
> **returns**: `List[TurnCandidate]`

\
`get_primary_candidate`
>```Python
>def get_primary_candidate() -> Union[TurnCandidate, None]
>```
>
> **Description**:\
> *returns primary turn candidate.*
> 
> **returns**: `TurnCandidate` or `None`

---

### `TurnCandidate` class
> representation of turn (message) content. 

fields:
- **candidate_id**: `str` - *Candidate id.*
- **text**: `str` - *Candidate text.*
- **fis_final**: `bool` - *Whether the candidate is final, i.e. completely generated.*
- **is_filtered**: `bool` - *Whether the candidate is filtered, i.e. safety truncated.*
- **create_time**: (optional) `datetime` - *Candidate creation time.*  

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
    - [message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/message.md) <- `(You're here.)`
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
