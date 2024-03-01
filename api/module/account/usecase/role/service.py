from typing import Optional

from interface.account import RoleCrud
from module.account.const import PROFILE_TYPE_CHOICE_ADMIN, PROFILE_TYPE_CHOICE_TENANT
from module.account.models import Pem, Role
from ninja import Query
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import RoleSchema
from util.error_util import ErrorUtil


class RoleService(RoleCrud):
    def get_role_list_with_filter(
        self, condition: Condition, order: str, filter: Query
    ) -> Result[QuerySet[RoleSchema]]:
        try:
            list_item = Role.objects.filter(**condition).order_by(order)
            return filter.filter(list_item), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_pem_option(self) -> list[dict]:
        queryset = Pem.objects.all()
        return [
            {"key": str(item.id), "title": item.module, "description": item.title}
            for item in queryset
        ]

    def get_profile_type_option(self, tenant_id: Optional[int]) -> list[dict]:
        profile_type_choice = (
            PROFILE_TYPE_CHOICE_TENANT if tenant_id else PROFILE_TYPE_CHOICE_ADMIN
        )
        return [{"value": item[0], "label": item[1]} for item in profile_type_choice]
