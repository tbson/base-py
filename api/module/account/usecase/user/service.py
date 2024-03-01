from typing import Callable, Optional

from contract.interface.account import Account, UserCrud
from ninja import Query
from contract.type.general import Condition, QuerySet
from contract.type.result import Result
from contract.type.schema import UserSchema


class UserService:
    @staticmethod
    def get_list_paging_user(user_crud_repo: UserCrud) -> Callable:
        def inner(
            tenant_id: Optional[int], order: str, filter: Query
        ) -> Result[QuerySet[UserSchema]]:
            condition: Condition = {
                "tenant_id": tenant_id,
            }
            return user_crud_repo.get_user_list_with_filter(condition, order, filter)

        return inner

    @staticmethod
    def get_user(account_repo: Account) -> Callable:
        def inner(id: int) -> Result[UserSchema]:
            return account_repo.get_user(dict(id=id))

        return inner

    @staticmethod
    def create_user(account_repo: Account) -> Callable:
        def inner(data: dict) -> Result[UserSchema]:
            return account_repo.create_user(data)

        return inner

    @staticmethod
    def update_user(account_repo: Account) -> Callable:
        def inner(id: int, data: dict) -> Result[UserSchema]:
            return account_repo.update_user(dict(id=id), data)

        return inner

    @staticmethod
    def delete_user(account_repo: Account) -> Callable:
        def inner(id: int) -> Result[list[int]]:
            return account_repo.delete_user(dict(id=id))

        return inner

    @staticmethod
    def delete_list_user(account_repo: Account) -> Callable:
        def inner(ids: list[int]) -> Result[list[int]]:
            return account_repo.delete_user(dict(id__in=ids))

        return inner
