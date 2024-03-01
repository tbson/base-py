from typing import Callable, Optional

from interface.account import Account, UserCrud
from ninja import Query
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import UserSchema


class UserLogic:
    @staticmethod
    def get_list_paging_user(user_crud_service: UserCrud) -> Callable:
        def inner(
            tenant_id: Optional[int], order: str, filter: Query
        ) -> Result[QuerySet[UserSchema]]:
            condition: Condition = {
                "tenant_id": tenant_id,
            }
            return user_crud_service.get_user_list_with_filter(condition, order, filter)

        return inner

    @staticmethod
    def get_user(account_service: Account) -> Callable:
        def inner(id: int) -> Result[UserSchema]:
            return account_service.get_user(dict(id=id))

        return inner

    @staticmethod
    def create_user(account_service: Account) -> Callable:
        def inner(data: dict) -> Result[UserSchema]:
            return account_service.create_user(data)

        return inner

    @staticmethod
    def update_user(account_service: Account) -> Callable:
        def inner(id: int, data: dict) -> Result[UserSchema]:
            return account_service.update_user(dict(id=id), data)

        return inner

    @staticmethod
    def delete_user(account_service: Account) -> Callable:
        def inner(id: int) -> Result[list[int]]:
            return account_service.delete_user(dict(id=id))

        return inner

    @staticmethod
    def delete_list_user(account_service: Account) -> Callable:
        def inner(ids: list[int]) -> Result[list[int]]:
            return account_service.delete_user(dict(id__in=ids))

        return inner
