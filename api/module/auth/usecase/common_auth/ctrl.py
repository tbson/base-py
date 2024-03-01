from typing import cast

from django.http import HttpRequest
from module.account.repo import AccountRepo
from module.auth.repo import AuthRepo
from module.auth.usecase.common_auth.repo import CommonAuthRepo
from module.auth.usecase.common_auth.service import (
    CommonAuthService,
    RefreshTokenOutput,
)
from module.auth.usecase.common_auth.validator import RefreshTokenInput
from ninja import Router
from contract.type.result import ErrorResponse, ErrorValue
from util.framework.authorization.auth_bearer import AuthBearer
from util.request_util import RequestUtil

router = Router()
TAGS = ["auth"]


@router.post("/logout/", tags=TAGS, response={200: dict, 400: ErrorValue})
def login(request: HttpRequest) -> dict | ErrorResponse:
    token = RequestUtil.get_token(request.headers)
    (result, ok) = CommonAuthService.logout(token)
    return result if ok else RequestUtil.err(result)


@router.post(
    "/refresh-token/", tags=TAGS, response={200: RefreshTokenOutput, 400: ErrorValue}
)
def refresh_token(
    request: HttpRequest, data: RefreshTokenInput
) -> RefreshTokenOutput | ErrorResponse:
    token = data.refresh_token
    auth_repo = AuthRepo()
    common_auth_repo = CommonAuthRepo()
    account_repo = AccountRepo()
    (result, ok) = CommonAuthService.refresh_token(
        auth_repo, common_auth_repo, account_repo
    )(token)
    return cast(RefreshTokenOutput, result) if ok else RequestUtil.err(result)


@router.get(
    "/refresh-check/",
    tags=TAGS,
    auth=AuthBearer(),
    response={200: dict, 400: ErrorValue},
)
def refresh_check(request: HttpRequest) -> dict | ErrorResponse:
    (result, ok) = CommonAuthService.refresh_check()
    return result if ok else RequestUtil.err(result)
