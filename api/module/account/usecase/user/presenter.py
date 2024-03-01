from typing import Callable, List

from module.account.models import User
from ninja import ModelSchema
from type.general import QuerySet
from type.schema import UserSchema
from util.framework.paging_util import PagingResponse, PagingUtil


class UserPresent(ModelSchema):
    full_name: str = ""
    role_ids: list[int] = []

    class Config:
        model = User
        model_fields = [
            "id",
            "email",
            "mobile",
            "first_name",
            "last_name",
            "tenant",
            "info",
            "is_active",
        ]


class UserListPresent(ModelSchema):
    full_name: str = ""

    class Config:
        model = User
        model_fields = [
            "id",
            "email",
            "mobile",
            "first_name",
            "last_name",
            "tenant",
            "info",
            "is_active",
        ]


class UserPagingPresent(PagingResponse):
    items: List[UserListPresent]

    @staticmethod
    def get_paging(page: int = 1) -> Callable:
        def inner(
            queryset: QuerySet[UserSchema], extra: dict = {}
        ) -> UserPagingPresent:
            data = PagingUtil.get_paging(UserListPresent, page)(queryset, extra)
            return UserPagingPresent(**data)

        return inner
