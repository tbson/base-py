import abc
from typing import Optional

from ninja import Query
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import PemSchema, RoleSchema, TenantSchema, UserSchema


class Account(abc.ABC):
    @abc.abstractmethod
    def get_list_tenant(self, condition: Condition) -> Result[QuerySet[TenantSchema]]:
        pass

    @abc.abstractmethod
    def get_tenant(self, condition: Condition) -> Result[TenantSchema]:
        pass

    @abc.abstractmethod
    def create_tenant(self, condition: Condition) -> Result[TenantSchema]:
        pass

    @abc.abstractmethod
    def update_tenant(self, condition: Condition, data: dict) -> Result[TenantSchema]:
        pass

    @abc.abstractmethod
    def delete_tenant(self, condition: Condition) -> Result[list[int]]:
        pass

    @abc.abstractmethod
    def get_list_role(self, condition: Condition) -> Result[QuerySet[RoleSchema]]:
        pass

    @abc.abstractmethod
    def get_role(self, condition: Condition) -> Result[RoleSchema]:
        pass

    @abc.abstractmethod
    def create_role(self, condition: Condition) -> Result[RoleSchema]:
        pass

    @abc.abstractmethod
    def update_role(self, condition: Condition, data: dict) -> Result[RoleSchema]:
        pass

    @abc.abstractmethod
    def delete_role(self, condition: Condition) -> Result[list[int]]:
        pass

    @abc.abstractmethod
    def get_list_pem(self, condition: Condition) -> Result[QuerySet[PemSchema]]:
        pass

    @abc.abstractmethod
    def get_pem(self, condition: Condition) -> Result[PemSchema]:
        pass

    @abc.abstractmethod
    def create_pem(self, condition: Condition) -> Result[PemSchema]:
        pass

    @abc.abstractmethod
    def update_pem(self, condition: Condition, data: dict) -> Result[PemSchema]:
        pass

    @abc.abstractmethod
    def delete_pem(self, condition: Condition) -> Result[list[int]]:
        pass

    @abc.abstractmethod
    def get_list_user(self, condition: Condition) -> Result[QuerySet[UserSchema]]:
        pass

    @abc.abstractmethod
    def get_user(self, condition: Condition) -> Result[UserSchema]:
        pass

    @abc.abstractmethod
    def create_user(self, condition: Condition) -> Result[UserSchema]:
        pass

    @abc.abstractmethod
    def update_user(self, condition: Condition, data: dict) -> Result[UserSchema]:
        pass

    @abc.abstractmethod
    def delete_user(self, condition: Condition) -> Result[list[int]]:
        pass


class UserCrud(abc.ABC):
    @abc.abstractmethod
    def get_user_list_with_filter(
        self, condition: Condition, order: str, filter: Query
    ) -> Result[QuerySet[UserSchema]]:
        pass


class RoleCrud(abc.ABC):
    @abc.abstractmethod
    def get_role_list_with_filter(
        self, condition: Condition, order: str, filter: Query
    ) -> Result[QuerySet[RoleSchema]]:
        pass


class AccountCommand(abc.ABC):
    @abc.abstractmethod
    def seeding_users(self) -> None:
        pass


class AccountSyncRole(abc.ABC):
    @abc.abstractmethod
    def sync_pems(self) -> dict[int, set[PemSchema]]:
        pass

    @abc.abstractmethod
    def sync_default_roles(self, tenant_id: Optional[int]) -> dict[int, RoleSchema]:
        pass

    @abc.abstractmethod
    def assign_roles_pems(
        self,
        role_map: dict[int, RoleSchema],
        profile_type_map: dict[int, set[PemSchema]],
    ) -> None:
        pass
