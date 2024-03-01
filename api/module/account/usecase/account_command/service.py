from typing import Callable, cast

from contract.interface.account import Account, AccountCommand, AccountSyncRole
from contract.type.general import QuerySet
from contract.type.schema import TenantSchema


class AccountCommandService:
    @staticmethod
    def sync_groups_pems(
        account_repo: Account,
        account_sync_role_repo: AccountSyncRole,
    ) -> Callable[[], None]:
        def inner() -> None:
            # sync pems
            profile_type_map = account_sync_role_repo.sync_pems()

            # sync system default roles
            system_role_map = account_sync_role_repo.sync_default_roles(None)

            # assign pems to system default roles
            account_sync_role_repo.assign_roles_pems(system_role_map, profile_type_map)

            # get all tenants
            tenants, _ok = account_repo.get_list_tenant({})
            if not _ok:
                return None
            tenants = cast(QuerySet[TenantSchema], tenants)
            for tenant in tenants:
                # sync tenant default roles
                tenant_role_map = account_sync_role_repo.sync_default_roles(tenant.id)

                # assign pems to tenant default roles
                account_sync_role_repo.assign_roles_pems(
                    tenant_role_map, profile_type_map
                )

        return inner

    @staticmethod
    def seeding_users(
        account_repo: Account,
        account_sync_role_repo: AccountSyncRole,
        account_command_repo: AccountCommand,
    ) -> Callable[[], None]:
        def inner() -> None:
            AccountCommandService.sync_groups_pems(
                account_repo, account_sync_role_repo
            )()
            account_command_repo.seeding_users()

        return inner
