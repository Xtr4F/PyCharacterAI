from typing import Union

from PyCharacterAI import methods

from PyCharacterAI.exceptions import AuthenticationError
from PyCharacterAI.requester import Requester


class BaseClient:
    def __init__(self, **kwargs):
        self.__token: Union[str, None] = None
        self.__web_next_auth: Union[str, None] = None
        self.__account_id: Union[str, None] = None

    # ========================================================== #
    # Use these only if you 100% know what are you doing.        #
    # It is recommended to use authenticate() method instead.    #
    # ========================================================== #

    def set_token(self, token: str):
        self.__token = token

    def set_web_next_auth(self, web_next_auth: str):
        self.__web_next_auth = web_next_auth

    def set_account_id(self, account_id: str):
        self.__account_id = account_id

    # ========================================================== #

    def get_token(self):
        return self.__token

    def get_web_next_auth(self):
        return self.__web_next_auth

    def get_account_id(self):
        return self.__account_id

    def get_headers(self, token=None, web_next_auth=None, include_web_next_auth=False):
        headers = {
            'authorization': f'Token {token or self.get_token()}',
            'Content-Type': 'application/json'
        }

        if include_web_next_auth:
            headers['cookie'] = web_next_auth or self.get_web_next_auth()

        return headers


class SyncClient(BaseClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__requester = Requester(**kwargs)

        self.account = methods.synchronous.AccountMethods(self, self.__requester)
        self.user = methods.synchronous.UserMethods(self, self.__requester)
        self.chat = methods.synchronous.ChatMethods(self, self.__requester)
        self.character = methods.synchronous.CharacterMethods(self, self.__requester)
        self.utils = methods.synchronous.UtilsMethods(self, self.__requester)

    def authenticate(self, token: str, **kwargs):
        self.set_token(token)

        web_next_auth: str = str(kwargs.get("web_next_auth", ""))

        if web_next_auth:
            self.set_web_next_auth(web_next_auth)

        try:
            self.set_account_id(str((self.account.fetch_me()).account_id))
        except Exception:
            raise AuthenticationError('Maybe your token is invalid?')


class AsyncClient(BaseClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__requester = Requester(**kwargs)

        self.account = methods.asynchronous.AccountMethods(self, self.__requester)
        self.user = methods.asynchronous.UserMethods(self, self.__requester)
        self.chat = methods.asynchronous.ChatMethods(self, self.__requester)
        self.character = methods.asynchronous.CharacterMethods(self, self.__requester)
        self.utils = methods.asynchronous.UtilsMethods(self, self.__requester)

    async def authenticate(self, token: str, **kwargs):
        self.set_token(token)

        web_next_auth: str = str(kwargs.get("web_next_auth", ""))

        if web_next_auth:
            self.set_web_next_auth(web_next_auth)

        try:
            self.set_account_id(str((await self.account.fetch_me()).account_id))
        except Exception:
            raise AuthenticationError('Maybe your token is invalid?')
