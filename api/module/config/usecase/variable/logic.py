from typing import Callable

from interface.config import Config, VariableCrud
from ninja import Query
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import VariableSchema


class VariableLogic:
    @staticmethod
    def get_list_paging_variable(variable_crud_service: VariableCrud) -> Callable:
        def inner(order: str, filter: Query) -> Result[QuerySet[VariableSchema]]:
            condition: Condition = {}
            return variable_crud_service.get_variable_list_with_filter(
                condition, order, filter
            )

        return inner

    @staticmethod
    def get_variable(config_service: Config) -> Callable:
        def inner(id: int) -> Result[VariableSchema]:
            return config_service.get_variable(dict(id=id))

        return inner

    @staticmethod
    def create_variable(config_service: Config) -> Callable:
        def inner(data: dict) -> Result[VariableSchema]:
            return config_service.create_variable(data)

        return inner

    @staticmethod
    def update_variable(config_service: Config) -> Callable:
        def inner(id: int, data: dict) -> Result[VariableSchema]:
            return config_service.update_variable(dict(id=id), data)

        return inner

    @staticmethod
    def delete_variable(config_service: Config) -> Callable:
        def inner(id: int) -> Result[list[int]]:
            return config_service.delete_variable(dict(id=id))

        return inner

    @staticmethod
    def delete_list_variable(config_service: Config) -> Callable:
        def inner(ids: list[int]) -> Result[list[int]]:
            return config_service.delete_variable(dict(id__in=ids))

        return inner
