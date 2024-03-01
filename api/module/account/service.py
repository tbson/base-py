from typing import Optional, cast

from django.utils.translation import gettext_lazy as _
from interface.account import Account
from module.account.models import Pem, Role, Tenant, User
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import PemSchema, RoleSchema, TenantSchema, UserSchema
from util.error_util import ErrorUtil
from util.framework.schema_util import SchemaUtil


class AccountService(Account):
    def get_list_tenant(
        self, condition: Condition, limit: Optional[int] = None, order_by: str = "-id"
    ) -> Result[QuerySet[TenantSchema]]:
        try:
            query = Tenant.objects.filter(**condition).order_by(order_by)
            if limit is not None:
                query = query[:limit]
            return query, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_tenant(self, condition: Condition) -> Result[TenantSchema]:
        try:
            return Tenant.objects.get(**condition), True
        except Tenant.DoesNotExist:
            err_msg = _("tenant does not exist")
            return ErrorUtil.format(err_msg), False

    def create_tenant(self, condition: Condition) -> Result[TenantSchema]:
        try:
            return Tenant.objects.create(**condition), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def update_tenant(self, condition: Condition, data: dict) -> Result[TenantSchema]:
        result, ok = self.get_tenant(condition)
        if not ok:
            return result, False
        tenant = result
        return SchemaUtil.update(tenant, data)

    def delete_tenant(self, condition: Condition) -> Result[list[int]]:
        try:
            tenants = Tenant.objects.filter(**condition)
            tenants.delete()
            return list(tenants.values_list("id", flat=True)), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_list_role(
        self, condition: Condition, limit: Optional[int] = None, order_by: str = "-id"
    ) -> Result[QuerySet[RoleSchema]]:
        try:
            query = Role.objects.filter(**condition).order_by(order_by)
            if limit is not None:
                query = query[:limit]
            return query, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_role(self, condition: Condition) -> Result[RoleSchema]:
        try:
            return Role.objects.get(**condition), True
        except Role.DoesNotExist:
            err_msg = _("role does not exist")
            return ErrorUtil.format(err_msg), False

    def create_role(self, condition: Condition) -> Result[RoleSchema]:
        try:
            pem_ids = cast(list[int], condition.pop("pem_ids", []))
            role = Role.objects.create(**condition)

            role.pems.set(Pem.objects.filter(id__in=pem_ids))
            return role, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def update_role(self, condition: Condition, data: dict) -> Result[RoleSchema]:
        result, ok = self.get_role(condition)
        if not ok:
            return result, False
        role = cast(RoleSchema, result)

        pem_ids = data.pop("pem_ids", None)
        if pem_ids is not None:
            role.pems.set(Pem.objects.filter(id__in=pem_ids))
        return SchemaUtil.update(role, data)

    def delete_role(self, condition: Condition) -> Result[list[int]]:
        try:
            roles = Role.objects.filter(**condition)
            roles.delete()
            return list(roles.values_list("id", flat=True)), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_list_pem(
        self, condition: Condition, limit: Optional[int] = None, order_by: str = "-id"
    ) -> Result[QuerySet[PemSchema]]:
        try:
            query = Pem.objects.filter(**condition).order_by(order_by)
            if limit is not None:
                query = query[:limit]
            return query, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_pem(self, condition: Condition) -> Result[PemSchema]:
        try:
            return Pem.objects.get(**condition), True
        except Pem.DoesNotExist:
            err_msg = _("pem does not exist")
            return ErrorUtil.format(err_msg), False

    def create_pem(self, condition: Condition) -> Result[PemSchema]:
        try:
            return Pem.objects.create(**condition), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def update_pem(self, condition: Condition, data: dict) -> Result[PemSchema]:
        result, ok = self.get_pem(condition)
        if not ok:
            return result, False
        pem = result
        return SchemaUtil.update(pem, data)

    def delete_pem(self, condition: Condition) -> Result[list[int]]:
        try:
            pems = Pem.objects.filter(**condition)
            pems.delete()
            return list(pems.values_list("id", flat=True)), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_list_user(
        self, condition: Condition, limit: Optional[int] = None, order_by: str = "-id"
    ) -> Result[QuerySet[UserSchema]]:
        try:
            query = User.objects.filter(**condition).order_by(order_by)
            if limit is not None:
                query = query[:limit]
            return query, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_user(self, condition: Condition) -> Result[UserSchema]:
        try:
            user = User.objects.get(**condition)
            return user, True
        except User.DoesNotExist:
            err_msg = _("user does not exist")
            return ErrorUtil.format(err_msg), False

    def create_user(self, condition: Condition) -> Result[UserSchema]:
        try:
            role_ids = cast(list[int], condition.pop("role_ids", []))
            password = condition.pop("password", None)
            user = User.objects.create(**condition)
            user.set_password(password)
            user.save()
            user.roles.set(Role.objects.filter(id__in=role_ids))
            return user, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def update_user(self, condition: Condition, data: dict) -> Result[UserSchema]:
        result, ok = self.get_user(condition)
        if not ok:
            return result, False
        user = cast(UserSchema, result)
        password = data.pop("password", None)
        if password is not None:
            user.set_password(password)
        role_ids = data.pop("role_ids", None)
        if role_ids is not None:
            user.roles.set(Role.objects.filter(id__in=role_ids))
        return SchemaUtil.update(user, data)

    def delete_user(self, condition: Condition) -> Result[list[int]]:
        try:
            users = User.objects.filter(**condition)
            users.delete()
            return list(users.values_list("id", flat=True)), True
        except Exception as e:
            return ErrorUtil.format(e), False
