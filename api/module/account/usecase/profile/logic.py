from typing import Callable, Optional

from interface.account import Account
from ninja import Schema
from type.result import Result
from type.schema import UserSchema


class ProfilePresent(Schema):
    email: str
    mobile: Optional[str]
    first_name: str
    last_name: str
    full_name: str


class ProfileLogic:
    @staticmethod
    def get_profile(
        account_service: Account,
    ) -> Callable[[int], Result[UserSchema]]:
        def inner(id: int) -> Result[UserSchema]:
            return account_service.get_user(dict(id=id))

        return inner

    @staticmethod
    def update_profile(
        account_service: Account,
    ) -> Callable[[int, dict], Result[UserSchema]]:
        def inner(id: int, data: dict) -> Result[UserSchema]:
            return account_service.update_user(dict(id=id), data)

        return inner
