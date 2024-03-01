from typing import cast

from django.http import HttpRequest
from module.account.service import AccountService
from module.account.usecase.profile.logic import ProfileLogic, ProfilePresent
from module.account.usecase.profile.validator import UpdateProfileInput
from ninja import Router
from type.result import ErrorResponse, ErrorValue
from util.framework.authorization.auth_bearer import AuthBearer
from util.request_util import RequestUtil

router = Router()

MODULE = "profile"
TAGS = ["account / manage profile"]


@router.get(
    "/",
    tags=TAGS,
    auth=AuthBearer(),
    response={200: ProfilePresent, 400: ErrorValue},
)
def get_profile(request: HttpRequest) -> ProfilePresent | ErrorResponse:
    user = request.user
    account_service = AccountService()
    result, ok = ProfileLogic.get_profile(account_service)(user.id)
    return cast(ProfilePresent, result) if ok else RequestUtil.err(result)


@router.put(
    "/",
    tags=TAGS,
    auth=AuthBearer(),
    response={200: ProfilePresent, 400: ErrorValue},
)
def update_update(
    request: HttpRequest, data: UpdateProfileInput
) -> ProfilePresent | ErrorResponse:
    user = request.user
    account_service = AccountService()
    result, ok = ProfileLogic.update_profile(account_service)(user.id, data.dict())
    return cast(ProfilePresent, result) if ok else RequestUtil.err(result)
