import abc

from ninja import Query
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import VariableSchema


class Config(abc.ABC):
    @abc.abstractmethod
    def get_list_variable(
        self, condition: Condition
    ) -> Result[QuerySet[VariableSchema]]:
        pass

    @abc.abstractmethod
    def get_variable(self, condition: Condition) -> Result[VariableSchema]:
        pass

    @abc.abstractmethod
    def create_variable(self, condition: Condition) -> Result[VariableSchema]:
        pass

    @abc.abstractmethod
    def update_variable(
        self, condition: Condition, data: dict
    ) -> Result[VariableSchema]:
        pass

    @abc.abstractmethod
    def delete_variable(self, condition: Condition) -> Result[list[int]]:
        pass


class VariableCrud(abc.ABC):
    @abc.abstractmethod
    def get_variable_list_with_filter(
        self, condition: Condition, order: str, filter: Query
    ) -> Result[QuerySet[VariableSchema]]:
        pass
