from typing import Optional, Union

from . import methods

from .requester import Requester


class BaseClient:
    def __init__(self):
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

    def get_headers(
        self,
        token: Optional[str] = None,
        web_next_auth: Optional[str] = None,
        include_web_next_auth: bool = False,
    ):
        headers = {
            "authorization": f"Token {token or self.get_token()}",
            "Content-Type": "application/json",
        }

        if include_web_next_auth:
            headers["cookie"] = web_next_auth or self.get_web_next_auth() or ""

        return headers


class AsyncClient(BaseClient):
    def __init__(self, **kwargs):
        super().__init__()

        self.__requester = Requester(**kwargs)

        self.account = methods.AccountMethods(self, self.__requester)
        self.user = methods.UserMethods(self, self.__requester)
        self.chat = methods.ChatMethods(self, self.__requester)
        self.character = methods.CharacterMethods(self, self.__requester)
        self.utils = methods.UtilsMethods(self, self.__requester)

    def _get_requester(self) -> Requester:
        return self.__requester

    async def authenticate(self, token: str, **kwargs):
        self.set_token(token)

        web_next_auth: str = str(kwargs.get("web_next_auth", ""))

        if web_next_auth:
            self.set_web_next_auth(web_next_auth)

        self.set_account_id(str((await self.account.fetch_me()).account_id))

    async def close_session(self) -> None:
        await self.__requester.ws_close_async()


async def get_client(token: str, **kwargs) -> AsyncClient:
    web_next_auth: str = str(kwargs.pop("web_next_auth", ""))

    client = AsyncClient(**kwargs)
    await client.authenticate(token=token, web_next_auth=web_next_auth)

    return client
