from typing import Callable, Optional

from contract.interface.account import Account
from ninja import Schema
from contract.type.result import Result
from contract.type.schema import UserSchema


class ProfilePresent(Schema):
    email: str
    mobile: Optional[str]
    first_name: str
    last_name: str
    full_name: str


class ProfileService:
    @staticmethod
    def get_profile(
        account_repo: Account,
    ) -> Callable[[int], Result[UserSchema]]:
        def inner(id: int) -> Result[UserSchema]:
            return account_repo.get_user(dict(id=id))

        return inner

    @staticmethod
    def update_profile(
        account_repo: Account,
    ) -> Callable[[int, dict], Result[UserSchema]]:
        def inner(id: int, data: dict) -> Result[UserSchema]:
            return account_repo.update_user(dict(id=id), data)

        return inner
