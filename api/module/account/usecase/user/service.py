from typing import Optional

from interface.account import UserCrud
from module.account.models import Role, User
from ninja import Query
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import UserSchema
from util.error_util import ErrorUtil


class UserService(UserCrud):
    def get_user_list_with_filter(
        self, condition: Condition, order: str, filter: Query
    ) -> Result[QuerySet[UserSchema]]:
        try:
            list_item = User.objects.filter(**condition).order_by(order)
            return filter.filter(list_item), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_role_option(self, tenant_id: Optional[int]) -> list[dict]:
        queryset = Role.objects.filter(tenant_id=tenant_id).order_by("title")
        return [
            {
                "value": item.id,
                "label": item.title,
            }
            for item in queryset
        ]
