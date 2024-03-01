from django.contrib.auth import get_user_model
from django.http import HttpRequest
from module.account.service import AccountService
from module.auth.service import AuthService
from module.auth.usecase.basic_auth.logic import (
    BasicAuthLogic,
    LoginOutput,
    ResetPwdOutput,
)
from module.auth.usecase.basic_auth.service import BasicAuthService
from module.auth.usecase.basic_auth.validator import (
    ChangePwdInput,
    LoginInput,
    ResetPwdInput,
)
from module.log.service import AuditLogService, LogService
from module.verify.service import VerifyService
from ninja import Router
from type.result import ErrorValue
from util.framework.authorization.auth_bearer import AuthBearer
from util.request_util import RequestUtil

User = get_user_model()


router = Router()

TAGS = ["auth"]


@router.post("/login/", tags=TAGS, response={200: LoginOutput, 400: ErrorValue})
def login(request: HttpRequest, data: LoginInput) -> dict:
    audit_log = AuditLogService(request, data.dict())
    result, ok = BasicAuthLogic.login(AuthService(), BasicAuthService(), LogService())(
        data.username, data.password
    )
    audit_log.log_login(result, ok)
    return result if ok else RequestUtil.err(result)


@router.post(
    "/change-pwd/",
    tags=TAGS,
    auth=AuthBearer(),
    response={200: dict, 400: ErrorValue},
)
def change_pwd(request: HttpRequest, data: ChangePwdInput) -> dict:
    user = request.user
    audit_log = AuditLogService(request, data.dict())
    result, ok = BasicAuthLogic.change_pwd(BasicAuthService(), LogService())(
        user, data.current_password, data.password, data.password_confirm
    )
    audit_log.log_change_pwd(result, ok, data.password)
    return result if ok else RequestUtil.err(result)


@router.post(
    "/reset-pwd/",
    tags=TAGS,
    response={200: ResetPwdOutput, 400: ErrorValue},
)
def reset_pwd(request: HttpRequest, data: ResetPwdInput) -> dict:
    audit_log = AuditLogService(request, data.dict())
    result, ok = BasicAuthLogic.reset_pwd(
        BasicAuthService(), AccountService(), VerifyService(), LogService()
    )(
        data.username,
        data.verify_id,
        data.verify_code,
        data.password,
        data.password_confirm,
    )
    audit_log.log_reset_pwd(result, ok, data.password)
    return result if ok else RequestUtil.err(result)
