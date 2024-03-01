import abc
from typing import Tuple

from type.general import Token
from type.result import Result
from type.schema import UserSchema


class Auth(abc.ABC):
    @abc.abstractmethod
    def get_user_from_token(self, access_token: Token) -> Result[UserSchema]:
        pass

    @abc.abstractmethod
    def update_last_login(self, user: UserSchema, refresh_token: Token) -> Result[None]:
        pass


class CommonAuth(abc.ABC):
    @abc.abstractmethod
    def update_refresh_token_signature(
        self, user: UserSchema, refresh_token: str
    ) -> Result[UserSchema]:
        pass


class BasicAuth(abc.ABC):
    @abc.abstractmethod
    def verify_username_password(
        self, username: str, password: str
    ) -> Result[UserSchema]:
        pass

    @abc.abstractmethod
    def generate_token_pair(self, user: UserSchema) -> Result[Tuple[Token, Token]]:
        pass

    @abc.abstractmethod
    def get_grouped_permission(self, user: UserSchema) -> Result[dict]:
        pass

    @abc.abstractmethod
    def ensure_match_pwd_confirm(
        self, password: str, password_confirm: str
    ) -> Result[None]:
        pass

    @abc.abstractmethod
    def ensure_match_old_pwd(self, user: UserSchema, old_password: str) -> Result[None]:
        pass

    @abc.abstractmethod
    def update_pwd(self, user: UserSchema, password: str) -> Result[UserSchema]:
        pass

    @abc.abstractmethod
    def update_last_change_pwd(self, user: UserSchema) -> Result[UserSchema]:
        pass

    @abc.abstractmethod
    def update_last_reset_pwd(self, user: UserSchema) -> Result[UserSchema]:
        pass

    @abc.abstractmethod
    def get_profile_type(self, user: UserSchema) -> int:
        pass
