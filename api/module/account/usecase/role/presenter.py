from typing import Callable, List

from module.account.models import Role
from ninja import ModelSchema
from type.general import QuerySet
from type.schema import RoleSchema
from util.framework.paging_util import PagingResponse, PagingUtil


class RolePresent(ModelSchema):
    pem_ids: list[int] = []
    profile_type_label: str = ""

    class Config:
        model = Role
        model_fields = [
            "id",
            "tenant",
            "profile_type",
            "title",
            "default",
        ]


class RoleListPresent(ModelSchema):
    profile_type_label: str = ""

    class Config:
        model = Role
        model_fields = [
            "id",
            "tenant",
            "profile_type",
            "title",
            "default",
        ]


class RolePagingPresent(PagingResponse):
    items: List[RoleListPresent]

    @staticmethod
    def get_paging(page: int = 1) -> Callable:
        def inner(
            queryset: QuerySet[RoleSchema], extra: dict = {}
        ) -> RolePagingPresent:
            data = PagingUtil.get_paging(RoleListPresent, page)(queryset, extra)
            return RolePagingPresent(**data)

        return inner
