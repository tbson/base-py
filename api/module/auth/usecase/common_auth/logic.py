from typing import Callable, cast

from interface.account import Account
from interface.auth import Auth, CommonAuth
from ninja import Schema
from type.general import Token
from type.result import ErrorValue, Result
from type.schema import UserSchema
from util.token_util import TokenUtil


class RefreshTokenOutput(Schema):
    token: Token
    refresh_token: Token


class CommonAuthLogic:
    @staticmethod
    def logout(token: Token) -> Result[dict]:
        # Do some cleanup here
        return {}, True

    @staticmethod
    def refresh_token(
        auth_service: Auth,
        common_auth_service: CommonAuth,
        account_service: Account,
    ) -> Callable[[Token], Result[RefreshTokenOutput]]:
        def inner(token: Token) -> Result[RefreshTokenOutput]:
            result, ok = TokenUtil.refresh_token(token)
            if not ok:
                result = cast(ErrorValue, result)
                return (result, False)

            (access_token, refresh_token) = result
            user_id = TokenUtil.get_id(refresh_token)
            result, ok = account_service.get_user(dict(id=user_id))
            if not ok:
                return (result, False)
            user = cast(UserSchema, result)
            result, ok = common_auth_service.update_refresh_token_signature(
                user, refresh_token
            )
            if not ok:
                return (result, False)

            update_last_login_result, ok = auth_service.update_last_login(
                user, refresh_token
            )
            if not ok:
                update_last_login_result = cast(ErrorValue, update_last_login_result)
                return (update_last_login_result, False)

            return (
                RefreshTokenOutput(token=access_token, refresh_token=refresh_token),
                True,
            )

        return inner

    @staticmethod
    def refresh_check() -> Result[dict]:
        return {}, True
