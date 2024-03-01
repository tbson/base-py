from typing import Callable

from contract.interface.account import Account, RoleCrud
from ninja import Query
from contract.type.general import Condition, QuerySet
from contract.type.result import Result
from contract.type.schema import RoleSchema


class RoleService:
    @staticmethod
    def get_list_paging_role(role_crud_repo: RoleCrud) -> Callable:
        def inner(order: str, filter: Query) -> Result[QuerySet[RoleSchema]]:
            condition: Condition = {}
            return role_crud_repo.get_role_list_with_filter(condition, order, filter)

        return inner

    @staticmethod
    def get_role(account_repo: Account) -> Callable:
        def inner(id: int) -> Result[RoleSchema]:
            return account_repo.get_role(dict(id=id))

        return inner

    @staticmethod
    def create_role(account_repo: Account) -> Callable:
        def inner(data: dict) -> Result[RoleSchema]:
            return account_repo.create_role(data)

        return inner

    @staticmethod
    def update_role(account_repo: Account) -> Callable:
        def inner(id: int, data: dict) -> Result[RoleSchema]:
            return account_repo.update_role(dict(id=id), data)

        return inner

    @staticmethod
    def delete_role(account_repo: Account) -> Callable:
        def inner(id: int) -> Result[list[int]]:
            return account_repo.delete_role(dict(id=id))

        return inner

    @staticmethod
    def delete_list_role(account_repo: Account) -> Callable:
        def inner(ids: list[int]) -> Result[list[int]]:
            return account_repo.delete_role(dict(id__in=ids))

        return inner
