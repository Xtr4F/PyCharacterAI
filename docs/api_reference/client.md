# Client
> Client - a class for user account interaction.

## Methods

## async `authenticate_as_guest()`
> Authenticates you as a guest *(There are limits on the number of messages, and some actions are not available)*

**Returns** `Client` instance 

  
## async `authenticate_with_token()`
> Authenticates you with a token

| Parameters | Description |
| --- | --- |
| **token** : `str` | `Access token`. (See how to get it in the `Getting started` section) |

**Returns** `Client` instance 

## `is_guest()`
> Returns `True` if the client is authenticated as a guest or `False` if it is authenticated with the token


## `is_authenticated()`
> Returns `False` if the client is authenticated as a guest or `True` if it is authenticated with the token


## async `fetch_categories()`
> Returns categories (`list[dict]`)


## async `fetch_user_config()`
> Returns the user config (`dict`)


## async `fetch_user()`
> Returns information about the user (`dict`)

- Example:
  ```Python
  user_info = await client.fetch_user()
  
  print(f"First name: {user_info['user']['first_name']} \n"
        f"Username: {user_info['user']['username']} \n"
        f"Id: {user_info['user']['id']}")
  ```

## async `fetch_featured_characters()`
> Returns list of featured characters (`list`)

- Example:
  ```Python
  featured_characters = await client.fetch_featured_characters()
  
  for character in featured_characters:
      print(f"Name : {character['participant__name']}, "
            f"Character_id : {character['external_id']}")
  ```

## async `fetch_characters_by_category()`
> Returns lists of characters by category 

| Parameters |
| --- |
| (*optional*) **curated** : `bool` = `False` | 

**Returns** `dict[str, list]`


## async `fetch_character_info()`
> Returns information about the character (`dict`)

| Parameters | 
| --- | 
| **character_id** : `str` | 

- Example:
  ```Python
  character_info = await client.fetch_character_info("iV5qb8ttzD7Ytl69U_-ONcW2tW_lrFrOVKExyKJHlJM")

    print(f"name: {character_info['name']} \n"
          f"title: {character_info['title']} \n"
          f"character_id: {character_info['external_id']}")
  ```
  > name: Lily \
  > title: Your friendly AI assistant \
  > character_id: iV5qb8ttzD7Ytl69U_-ONcW2tW_lrFrOVKExyKJHlJM


## async `search_characters()`
> ⚠️ To use this method, you must be authenticated with a token
>
> Searches for characters by name

| Parameters |
| --- | 
| **character_name** : `str` | 

- Example:
  ```Python
  search_results = await client.search_characters("Catgirl")  # Why not.

  for result in search_results:
      print(f"Name: {result['participant__name']}, "
            f"Character ID: {result['external_id']}")
  ```

  > Name: Brazilian Catgirl, Character ID: vYZ06E9v4omBZT3OIuserO1-CQfiVMsaoKnnjt2KdGU \
  > Name: Homeless Catgirl, Character ID: VTRhHLmc0cIQJhoscsqRLWcJPJioUXc0pja6w6Ri7OY \
  > Name: Catgirl maid Kitty, Character ID: qVj_CJkVTHVwBgLZ50s2mlXUhTYAcb3_5JrRmM4kBr0 \
  > Name: The catgirl twins, Character ID: mhbuLkwjQnlNKHHybATY3DQC0fK-wHpWqIt4S0bNhQk 
  > 
  > ... And 106 more catgirls ...

**Returns** `list`

  
## async `get_recent_conversations()`
> Returns a list of characters you recently had a conversation with. (`list`)

## async `generate_image()`
> Generates an image by prompt


| Parameters | Description |
| --- | --- |
|  **prompt** : `str` | Text description of the image |

**Returns** `str` (link to the image on the Character AI server)

## async `upload_image()`
> Uploads the image to the CharacterAI server. (Supported image formats
> are PNG, JPEG, WEBP)

| Parameters | Description |
| --- | --- |
|  **image** : `str` | Link or path to the image |

**Returns** `str` (link to the image on the Character AI server)

## async `generate_voice()`
> Synthesizing text into audio using different voices

| Parameters | Description |
| --- | --- |
|  **voice_id** : `int` | voice id |
| **prompt** : `str` | text to be voiced |

**Returns** `BytesIO | None`



## async `create_chat()`
> Creates a new chat with character

| Parameters | 
| --- |
| **character_id** : `str` |

**Returns** `Chat` instance

## async `continue_chat()`
> Returns chat with character by its `history_id`

| Parameters | 
| --- | 
| **character_id** : `str | None` = `None` |
| **history_id** : `str` |

**Returns** `Chat` instance


## async `create_or_continue_chat()`
> Returns chat with character or creates a new one, if there was none

| Parameters | 
| --- | 
| **character_id** : `str` | 
| (*optional*) **history_id** : `str` = `None` |

**Returns** `Chat` instance



## 📖:
- [Welcome](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/welcome.md) 
- [Getting started](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/getting_started.md)
- API Reference:
  - [Client](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/client.md) <- `(You're here.)`
  - [Chat](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/chat.md)
  - Messages:
    - [Message](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/messages/message.md)
    - [Reply](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/messages/reply.md)
    - [MessageHistory](https://github.com/Xtr4F/PyCharacterAI/blob/main/docs/api_reference/messages/message_history.md)