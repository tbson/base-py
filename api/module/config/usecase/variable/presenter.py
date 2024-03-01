from typing import Callable, List

from module.config.models import Variable
from ninja import ModelSchema
from type.general import QuerySet
from type.schema import VariableSchema
from util.framework.paging_util import PagingResponse, PagingUtil


class VariablePresent(ModelSchema):
    type_label: str = ""

    class Config:
        model = Variable
        model_fields = [
            "id",
            "uid",
            "value",
            "description",
            "type",
        ]


class VariableListPresent(ModelSchema):
    type_label: str = ""

    class Config:
        model = Variable
        model_fields = [
            "id",
            "uid",
            "value",
            "type",
        ]


class VariablePagingPresent(PagingResponse):
    items: List[VariableListPresent]

    @staticmethod
    def get_paging(page: int = 1) -> Callable:
        def inner(
            queryset: QuerySet[VariableSchema], extra: dict = {}
        ) -> VariablePagingPresent:
            data = PagingUtil.get_paging(VariableListPresent, page)(queryset, extra)
            return VariablePagingPresent(**data)

        return inner
