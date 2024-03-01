from typing import Callable, cast

from interface.account import Account, AccountCommand, AccountSyncRole
from type.general import QuerySet
from type.schema import TenantSchema


class AccountCommandLogic:
    @staticmethod
    def sync_groups_pems(
        account_service: Account,
        account_sync_role_service: AccountSyncRole,
    ) -> Callable[[], None]:
        def inner() -> None:
            # sync pems
            profile_type_map = account_sync_role_service.sync_pems()

            # sync system default roles
            system_role_map = account_sync_role_service.sync_default_roles(None)

            # assign pems to system default roles
            account_sync_role_service.assign_roles_pems(
                system_role_map, profile_type_map
            )

            # get all tenants
            tenants, _ok = account_service.get_list_tenant({})
            if not _ok:
                return None
            tenants = cast(QuerySet[TenantSchema], tenants)
            for tenant in tenants:
                # sync tenant default roles
                tenant_role_map = account_sync_role_service.sync_default_roles(
                    tenant.id
                )

                # assign pems to tenant default roles
                account_sync_role_service.assign_roles_pems(
                    tenant_role_map, profile_type_map
                )

        return inner

    @staticmethod
    def seeding_users(
        account_service: Account,
        account_sync_role_service: AccountSyncRole,
        account_command_service: AccountCommand,
    ) -> Callable[[], None]:
        def inner() -> None:
            AccountCommandLogic.sync_groups_pems(
                account_service, account_sync_role_service
            )()
            account_command_service.seeding_users()

        return inner
