from typing import Optional

from django.http import HttpRequest
from module.account.const import ProfileType
from module.account.repo import AccountRepo
from module.account.usecase.user.service import UserService
from module.account.usecase.user.presenter import UserPagingPresent, UserPresent
from module.account.usecase.user.repo import UserRepo
from module.account.usecase.user.validator import CreateUserInput, UpdateUserInput
from ninja import Field, FilterSchema, Query, Router
from contract.type.result import ErrorResponse, ErrorValue
from util.framework.authorization.auth_rbac import AuthRbac
from util.request_util import RequestUtil

router = Router()

MODULE = "user"
TAGS = ["account / manage user"]


class Filter(FilterSchema):
    profile_type: Optional[int] = None
    q: Optional[str] = Field(
        None,
        q=[
            "email__icontains",
            "mobile__icontains",
            "first_name__icontains",
            "last_name__icontains",
        ],
    )


@router.get(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "get_list", [ProfileType.STAFF]),
    response={200: UserPagingPresent, 400: ErrorValue},
)
def get_list(
    request: HttpRequest, page: int = 1, order: str = "-id", filter: Filter = Query(...)
) -> UserPagingPresent | ErrorResponse:
    user_repo = UserRepo()
    user = request.user
    result, ok = UserService.get_list_paging_user(user_repo)(
        user.tenant_id, order, filter
    )
    if not ok:
        return RequestUtil.err(result)
    role_option = UserRepo().get_role_option(request.user.tenant_id)
    return UserPagingPresent.get_paging(page)(result, {"option": {"role": role_option}})


@router.get(
    "/{id}",
    tags=TAGS,
    auth=AuthRbac(MODULE, "get_item", [ProfileType.STAFF]),
    response={200: UserPresent, 400: ErrorValue},
)
def get_item(request: HttpRequest, id: int) -> UserPresent | ErrorResponse:
    account_repo = AccountRepo()
    result, ok = UserService.get_user(account_repo)(id)
    return result if ok else RequestUtil.err(result)


@router.post(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "create", [ProfileType.STAFF]),
    response={200: UserPresent, 400: ErrorValue},
)
def create(request: HttpRequest, data: CreateUserInput) -> UserPresent | ErrorResponse:
    account_repo = AccountRepo()
    result, ok = UserService.create_user(account_repo)(data.dict())
    return result if ok else RequestUtil.err(result)


@router.put(
    "/{id}",
    tags=TAGS,
    auth=AuthRbac(MODULE, "update", [ProfileType.STAFF]),
    response={200: UserPresent, 400: ErrorValue},
)
def update(
    request: HttpRequest, id: int, data: UpdateUserInput
) -> UserPresent | ErrorResponse:
    account_repo = AccountRepo()
    result, ok = UserService.update_user(account_repo)(
        id, data.dict(exclude_unset=True)
    )
    return result if ok else RequestUtil.err(result)


@router.delete(
    "/{id}",
    tags=TAGS,
    auth=AuthRbac(MODULE, "delete", [ProfileType.STAFF]),
    response={200: list[int], 400: ErrorValue},
)
def delete(request: HttpRequest, id: int) -> list[int] | ErrorResponse:
    account_repo = AccountRepo()
    result, ok = UserService.delete_user(account_repo)(id)
    return result if ok else RequestUtil.err(result)


@router.delete(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "delete_list", [ProfileType.STAFF]),
    response={200: list[int], 400: ErrorValue},
)
def delete_list(request: HttpRequest, ids: str) -> list[int] | ErrorResponse:
    id_list = ids.split(",")
    account_repo = AccountRepo()
    result, ok = UserService.delete_list_user(account_repo)(id_list)
    return result if ok else RequestUtil.err(result)
