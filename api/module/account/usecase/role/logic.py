from typing import Callable

from interface.account import Account, RoleCrud
from ninja import Query
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import RoleSchema


class RoleLogic:
    @staticmethod
    def get_list_paging_role(role_crud_service: RoleCrud) -> Callable:
        def inner(order: str, filter: Query) -> Result[QuerySet[RoleSchema]]:
            condition: Condition = {}
            return role_crud_service.get_role_list_with_filter(condition, order, filter)

        return inner

    @staticmethod
    def get_role(account_service: Account) -> Callable:
        def inner(id: int) -> Result[RoleSchema]:
            return account_service.get_role(dict(id=id))

        return inner

    @staticmethod
    def create_role(account_service: Account) -> Callable:
        def inner(data: dict) -> Result[RoleSchema]:
            return account_service.create_role(data)

        return inner

    @staticmethod
    def update_role(account_service: Account) -> Callable:
        def inner(id: int, data: dict) -> Result[RoleSchema]:
            return account_service.update_role(dict(id=id), data)

        return inner

    @staticmethod
    def delete_role(account_service: Account) -> Callable:
        def inner(id: int) -> Result[list[int]]:
            return account_service.delete_role(dict(id=id))

        return inner

    @staticmethod
    def delete_list_role(account_service: Account) -> Callable:
        def inner(ids: list[int]) -> Result[list[int]]:
            return account_service.delete_role(dict(id__in=ids))

        return inner
