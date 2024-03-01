from django.contrib.auth import get_user_model
from django.http import HttpRequest
from module.account.repo import AccountRepo
from module.auth.repo import AuthRepo
from module.auth.usecase.basic_auth.service import (
    BasicAuthService,
    LoginOutput,
    ResetPwdOutput,
)
from module.auth.usecase.basic_auth.repo import BasicAuthRepo
from module.auth.usecase.basic_auth.validator import (
    ChangePwdInput,
    LoginInput,
    ResetPwdInput,
)
from module.log.repo import AuditLogRepo, LogRepo
from module.verify.repo import VerifyRepo
from ninja import Router
from contract.type.result import ErrorValue
from util.framework.authorization.auth_bearer import AuthBearer
from util.request_util import RequestUtil

User = get_user_model()


router = Router()

TAGS = ["auth"]


@router.post("/login/", tags=TAGS, response={200: LoginOutput, 400: ErrorValue})
def login(request: HttpRequest, data: LoginInput) -> dict:
    audit_log = AuditLogRepo(request, data.dict())
    result, ok = BasicAuthService.login(AuthRepo(), BasicAuthRepo(), LogRepo())(
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
    audit_log = AuditLogRepo(request, data.dict())
    result, ok = BasicAuthService.change_pwd(BasicAuthRepo(), LogRepo())(
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
    audit_log = AuditLogRepo(request, data.dict())
    result, ok = BasicAuthService.reset_pwd(
        BasicAuthRepo(), AccountRepo(), VerifyRepo(), LogRepo()
    )(
        data.username,
        data.verify_id,
        data.verify_code,
        data.password,
        data.password_confirm,
    )
    audit_log.log_reset_pwd(result, ok, data.password)
    return result if ok else RequestUtil.err(result)
