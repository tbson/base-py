from typing import cast

from django.http import HttpRequest
from module.account.service import AccountService
from module.auth.service import AuthService
from module.auth.usecase.common_auth.logic import CommonAuthLogic, RefreshTokenOutput
from module.auth.usecase.common_auth.service import CommonAuthService
from module.auth.usecase.common_auth.validator import RefreshTokenInput
from ninja import Router
from type.result import ErrorResponse, ErrorValue
from util.framework.authorization.auth_bearer import AuthBearer
from util.request_util import RequestUtil

router = Router()
TAGS = ["auth"]


@router.post("/logout/", tags=TAGS, response={200: dict, 400: ErrorValue})
def login(request: HttpRequest) -> dict | ErrorResponse:
    token = RequestUtil.get_token(request.headers)
    (result, ok) = CommonAuthLogic.logout(token)
    return result if ok else RequestUtil.err(result)


@router.post(
    "/refresh-token/", tags=TAGS, response={200: RefreshTokenOutput, 400: ErrorValue}
)
def refresh_token(
    request: HttpRequest, data: RefreshTokenInput
) -> RefreshTokenOutput | ErrorResponse:
    token = data.refresh_token
    auth_service = AuthService()
    common_auth_service = CommonAuthService()
    account_service = AccountService()
    (result, ok) = CommonAuthLogic.refresh_token(
        auth_service, common_auth_service, account_service
    )(token)
    return cast(RefreshTokenOutput, result) if ok else RequestUtil.err(result)


@router.get(
    "/refresh-check/",
    tags=TAGS,
    auth=AuthBearer(),
    response={200: dict, 400: ErrorValue},
)
def refresh_check(request: HttpRequest) -> dict | ErrorResponse:
    (result, ok) = CommonAuthLogic.refresh_check()
    return result if ok else RequestUtil.err(result)
