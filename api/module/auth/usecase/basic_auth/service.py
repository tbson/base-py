from typing import Callable, cast

from contract.interface.account import Account
from contract.interface.auth import Auth, BasicAuth
from contract.interface.log import Log
from contract.interface.verify import Verify
from ninja import Schema
from contract.type.general import Permissions, ProfileType, Token
from contract.type.result import ErrorValue, Result
from contract.type.schema import OtpSchema, UserSchema


class LoginOutput(Schema):
    token: Token
    refresh_token: Token
    profile_type: ProfileType
    permissions: Permissions
    full_name: str = ""


class ResetPwdOutput(Schema):
    target: str


class BasicAuthService:
    @staticmethod
    def login(auth_repo: Auth, basic_auth_repo: BasicAuth, log_repo: Log) -> Callable:
        def inner(
            username: str,
            password: str,
        ) -> Result[LoginOutput]:
            (result, ok) = log_repo.reached_login_fail_limit(username)
            if not ok:
                result = cast(ErrorValue, result)
                return (result, False)

            (result, ok) = basic_auth_repo.verify_username_password(username, password)
            if not ok:
                return (result, False)
            user = cast(UserSchema, result)

            (token_result, ok) = basic_auth_repo.generate_token_pair(user)
            if not ok:
                token_result = cast(ErrorValue, token_result)
                return (token_result, False)
            (token, refresh_token) = token_result

            (result, ok) = basic_auth_repo.get_grouped_permission(user)
            if not ok:
                return (result, False)
            permissions = result

            (result, ok) = auth_repo.update_last_login(user, refresh_token)
            if not ok:
                result = cast(ErrorValue, result)
                return (result, False)

            return (
                LoginOutput(
                    token=token,
                    refresh_token=refresh_token,
                    profile_type=basic_auth_repo.get_profile_type(user),
                    permissions=permissions,
                    full_name=user.full_name,
                ),
                True,
            )

        return inner

    @staticmethod
    def change_pwd(basic_auth_repo: BasicAuth, log_repo: Log) -> Callable:
        def inner(
            user: UserSchema,
            current_password: str,
            password: str,
            password_confirm: str,
        ) -> Result[dict]:
            (result, ok) = log_repo.is_use_old_password(user.username, password)
            if not ok:
                result = cast(ErrorValue, result)
                return result, False
            (result, ok) = basic_auth_repo.ensure_match_pwd_confirm(
                password, password_confirm
            )
            if not ok:
                result = cast(ErrorValue, result)
                return result, False

            (result, ok) = basic_auth_repo.ensure_match_old_pwd(user, current_password)
            if not ok:
                result = cast(ErrorValue, result)
                return result, False

            (result, ok) = basic_auth_repo.update_pwd(user, password)
            if not ok:
                return result, False

            user = result
            basic_auth_repo.update_last_change_pwd(user)
            return {}, True

        return inner

    @staticmethod
    def reset_pwd(
        basic_auth_repo: BasicAuth,
        account_repo: Account,
        verify_repo: Verify,
        log_repo: Log,
    ) -> Callable:
        def inner(
            username: str,
            verify_id: str,
            verify_code: str,
            password: str,
            password_confirm: str,
        ) -> Result[dict]:
            (result, ok) = log_repo.is_use_old_password(username, password)
            if not ok:
                result = cast(ErrorValue, result)
                return result, False
            (result, ok) = verify_repo.verify_otp(verify_id, verify_code)
            if not ok:
                return result, False
            otp = cast(OtpSchema, result)
            target = otp.target
            (result, ok) = account_repo.get_user(dict(email=target))
            if not ok or target != username:
                return result, False
            user = result
            (result, ok) = basic_auth_repo.ensure_match_pwd_confirm(
                password, password_confirm
            )
            if not ok:
                result = cast(ErrorValue, result)
                return result, False
            (result, ok) = basic_auth_repo.update_pwd(user, password)

            user = result
            (result, ok) = basic_auth_repo.update_last_reset_pwd(user)

            return (ResetPwdOutput(target=target), True) if ok else (result, False)

        return inner
