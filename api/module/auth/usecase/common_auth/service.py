from interface.auth import CommonAuth
from type.result import Result
from type.schema import UserSchema
from util.error_util import ErrorUtil
from util.token_util import TokenUtil


class CommonAuthService(CommonAuth):
    def update_refresh_token_signature(
        self, user: UserSchema, refresh_token: str
    ) -> Result[UserSchema]:
        try:
            refresh_token_signature = TokenUtil.get_token_signature(refresh_token)
            user.refresh_token_signature = refresh_token_signature
            user.save()
            return user, True
        except Exception as e:
            return ErrorUtil.format(e), False
