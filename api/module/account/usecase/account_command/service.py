from typing import cast

from django.conf import settings
from interface.account import AccountCommand
from type.schema import UserSchema
from module.account.const import (
    PROFILE_TYPE_DICT,
    ProfileType,
)
from module.account.models import Role
from module.account.service import AccountService


class AccountCommandService(AccountCommand):
    def seeding_users(self) -> None:
        password = settings.SAMPLE_PASSWORD
        list_data = {
            ProfileType.ADMIN: {
                "email": "admin@localhost",
                "password": password,
                "first_name": "Admin",
                "last_name": "Account",
            },
            ProfileType.STAFF: {
                "email": "staff@localhost",
                "password": password,
                "first_name": "Staff",
                "last_name": "Account",
            },
        }
        for profile_type, data in list_data.items():
            group = Role.objects.get(title=PROFILE_TYPE_DICT[profile_type])
            user, ok = AccountService().create_user(data)
            if ok:
                user = cast(UserSchema, user)
                user.roles.add(group)
                if profile_type == ProfileType.ADMIN:
                    user.is_superuser = True
                    user.is_staff = True
                user.save()
