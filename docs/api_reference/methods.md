# Methods

Here's a list of all the methods. All methods are grouped into 5 groups: `account`, `character`, `chat`, `user` and `utils`. For example, to call an account method, you have to do something like: 
```Python
client.account.method()
```

---
| [**account**](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/account.md) |
|---|
| `async` **fetch_me** |
| `async` **fetch_my_settings** |
| `async` **fetch_my_followers** |
| `async` **fetch_my_following** |
| `async` **fetch_my_persona** |
| `async` **fetch_my_personas** |
| `async` **fetch_my_characters** |
| `async` **fetch_my_upvoted_characters** |
| `async` **fetch_my_voices** |
| `async` **edit_account** |
| `async` **create_persona** |
| `async` **edit_persona** |
| `async` **delete_persona** |
| `async` **set_default_persona** |
| `async` **unset_default_persona** |
| `async` **set_persona** |
| `async` **unset_persona** |
| `async` **set_voice** |
| `async` **unset_voice** |

---

| [**character**](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/character.md) |
| --- |
| `async` **fetch_characters_by_category** |
| `async` **fetch_recommended_characters** |
| `async` **fetch_featured_characters** |
| `async` **fetch_similar_characters** |
| `async` **fetch_character_info** |
| `async` **search_characters** |
| `async` **search_creators** |
| `async` **character_vote** |
| `async` **create_character** |
| `async` **edit_character** |

---

| [**chat**](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/chat.md) |
|-------------------------------------------------------------------------------------------------|
| `async` **fetch_histories**                                                                     |
| `async` **fetch_chats**                                                                         |
| `async` **fetch_chat**                                                                          |
| `async` **fetch_recent_chats**                                                                  |
| `async` **fetch_messages**                                                                      |
| `async` **fetch_all_messages**                                                                  |
| `async` **fetch_following_messages**                                                            |
| `async` **fetch_pinned_messages**                                                               |
| `async` **fetch_all_pinned_messages**                                                           |
| `async` **update_chat_name**                                                                    |
| `async` **archive_chat**                                                                        |
| `async` **unarchive_chat**                                                                                  |
| `async` **copy_chat**                                                                                    |
| `async` **create_chat**                                                                         |
| `async` **update_primary_candidate**                                                            |
| `async` **send_message**                                                                        |
| `async` **another_response**                                                                    |
| `async` **edit_message**
| `async` **delete_messages**                                                                     |
| `async` **delete_message**                                                                      |
| `async` **pin_message**                                                                         |
| `async` **unpin_message**                                                                       |

---

| [**user**](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/user.md) |
| --- |
| `async` **fetch_user** |
| `async` **fetch_user_voices** |
| `async` **follow_user** |
| `async` **unfollow_user** |

---

| [**utils**](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods/utils.md) |
| --- |
| `async` **ping** |
| `async` **fetch_voice** |
| `async` **search_voices** |
| `async` **generate_image** |
| `async` **upload_avatar** |
| `async` **upload_voice** |
| `async` **edit_voice** |
| `async` **delete_voice** |
| `async` **generate_speech** |

--- 

## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md)
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md)
- API Reference:
  - [methods](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/methods.md): <- `(You're here.)`
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
    - [media](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/types/media.md)
