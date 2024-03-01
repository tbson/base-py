from typing import cast

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from interface.auth import Auth
from type.general import Token
from type.result import Result
from type.schema import UserSchema
from util.date_util import DateUtil
from util.error_util import ErrorUtil
from util.token_util import TokenUtil

User = get_user_model()


class AuthService(Auth):
    def get_user_from_token(self, access_token: Token) -> Result[UserSchema]:
        (result, ok) = TokenUtil.decode(access_token)
        if not ok:
            return (result, False)
        decoded = cast(dict, result)
        user_id = int(decoded.get("user_id", "0"))
        try:
            user = User.objects.get(id=user_id)
            return (user, True)
        except User.DoesNotExist:
            error_message = _("user not found")
            return (ErrorUtil().format(error_message), False)

    def update_last_login(self, user: UserSchema, refresh_token: Token) -> Result[None]:
        try:
            user.refresh_token_signature = TokenUtil.get_token_signature(refresh_token)
            user.last_login = DateUtil.now()
            user.save()
            return (None, True)
        except Exception:
            error_message = _("failed to update last login time")
            return (ErrorUtil.format(error_message), False)
