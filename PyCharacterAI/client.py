from typing import Union

from .methods import ChatMethods, AccountMethods, CharacterMethods, UserMethods, UtilsMethods
from .exceptions import AuthenticationError
from .requester import Requester


class Client:
    def __init__(self, **kwargs):
        self.__token: Union[str, None] = None
        self.__web_next_auth: Union[str, None] = None
        self.__account_id: Union[str, None] = None

        self.__requester = Requester(**kwargs)

        self.account = AccountMethods(self, self.__requester)
        self.user = UserMethods(self, self.__requester)
        self.chat = ChatMethods(self, self.__requester)
        self.character = CharacterMethods(self, self.__requester)
        self.utils = UtilsMethods(self, self.__requester)

    async def authenticate(self, token: str, **kwargs):
        self.set_token(token)

        web_next_auth: str = str(kwargs.get("web_next_auth", ""))

        if web_next_auth:
            self.set_web_next_auth(web_next_auth)

        try:
            self.set_account_id(str((await self.account.fetch_me()).account_id))
        except Exception:
            raise AuthenticationError('Maybe your token is invalid?')

    async def close_session(self):
        await self.__requester.ws_close()

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
