from typing import Tuple

from django.utils.translation import gettext_lazy as _
from interface.auth import BasicAuth
from module.account.const import ProfileType
from module.account.models import Pem, User
from type.general import Token
from type.result import Result
from type.schema import UserSchema
from util.date_util import DateUtil
from util.error_util import ErrorUtil
from util.token_util import TokenUtil


class BasicAuthService(BasicAuth):
    def verify_username_password(
        self, username: str, password: str
    ) -> Result[UserSchema]:
        error_message = _("incorrect login information, please try again")
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                msg = _("account is not active")
                return (ErrorUtil.format(msg), False)
            if not user.check_password(password):
                return (ErrorUtil.format(error_message), False)
            return (user, True)
        except User.DoesNotExist:
            return (ErrorUtil.format(error_message), False)

    def generate_token_pair(self, user: UserSchema) -> Result[Tuple[Token, Token]]:
        permission_ids = list(
            Pem.objects.filter(roles__in=user.roles.all())
            .distinct()
            .values_list("id", flat=True)
        )
        refresh_token = TokenUtil.encode_refresh_token(user.id)
        token = TokenUtil.encode_access_token(user.id, permission_ids)
        return ((token, refresh_token), True)

    def get_grouped_permission(self, user: UserSchema) -> Result[dict]:
        try:
            role_ids = user.roles.values_list("id", flat=True)
            if user.is_staff or user.is_superuser:
                queryset = Pem.objects.all()
            else:
                queryset = Pem.objects.filter(roles__in=role_ids).distinct()
            list_item = list(queryset.values_list("module", "action"))
            result: dict = {}
            for module, action in list_item:
                result[module] = result.get(module, []) + [action]
            return (result, True)
        except Exception:
            error_message = _("failed to get permissions")
            return (ErrorUtil.format(error_message), False)

    def ensure_match_pwd_confirm(
        self, password: str, password_confirm: str
    ) -> Result[None]:
        error_message = _("password and confirm password didn't match")
        return (
            (ErrorUtil.format(error_message), False)
            if password != password_confirm
            else (None, True)
        )

    def ensure_match_old_pwd(self, user: UserSchema, old_password: str) -> Result[None]:
        error_message = _("incorrect current password")
        if not user.check_password(old_password):
            return ErrorUtil.format(error_message), False
        return None, True

    def update_pwd(self, user: UserSchema, password: str) -> Result[UserSchema]:
        try:
            user.set_password(password)
            user.save()
            return (user, True)
        except Exception:
            error_message = _("failed to update password")
            return (ErrorUtil.format(error_message), False)

    def update_last_change_pwd(self, user: UserSchema) -> Result[UserSchema]:
        try:
            user.last_change_pwd = DateUtil.now()
            user.save()
            return user, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def update_last_reset_pwd(self, user: UserSchema) -> Result[UserSchema]:
        try:
            user.last_reset_pwd = DateUtil.now()
            user.save()
            return user, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_profile_type(self, user: UserSchema) -> int:
        try:
            return min(list(user.roles.values_list("profile_type", flat=True)))
        except Exception as e:
            print(e)
            return ProfileType.USER
