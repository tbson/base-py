from typing import Optional
from interface.account import AccountSyncRole
from util.framework.authorization.auth_rbac import AuthRbacUtil
from type.schema import RoleSchema, PemSchema
from module.account.models import Role, Pem
from module.account.const import (
    SYSTEM_PROFILE_TYPES,
    TENANT_PROFILE_TYPES,
    PROFILE_TYPE_DICT,
)


class AccountSyncRoleService(AccountSyncRole):
    def sync_pems(self) -> dict[int, set[PemSchema]]:
        pem_list = AuthRbacUtil.get_pem_list()
        profile_type_map: dict[int, set[PemSchema]] = {}
        for module, action, profile_types in pem_list:
            module_label = module.replace("_", " ")
            action_label = action.replace("_", " ")
            pem, _ = Pem.objects.get_or_create(
                module=module,
                action=action,
                defaults={"title": f"{action_label} {module_label}"},
            )
            for profile_type in profile_types:
                if profile_type not in profile_type_map:
                    profile_type_map[profile_type] = set()
                profile_type_map[profile_type].add(pem)
        return profile_type_map

    def sync_default_roles(self, tenant_id: Optional[int]) -> dict[int, RoleSchema]:
        profile_types = (
            SYSTEM_PROFILE_TYPES if tenant_id is None else TENANT_PROFILE_TYPES
        )
        role_map = {}
        for profile_type in profile_types:
            name = PROFILE_TYPE_DICT.get(profile_type)
            role, _ = Role.objects.get_or_create(
                tenant_id=tenant_id, title=name, profile_type=profile_type, default=True
            )
            role_map[profile_type] = role
        return role_map

    def assign_roles_pems(
        self,
        role_map: dict[int, RoleSchema],
        profile_type_map: dict[int, set[PemSchema]],
    ) -> None:
        for profile_type, role in role_map.items():
            pems = profile_type_map.get(profile_type, set())
            role.pems.set(pems)
