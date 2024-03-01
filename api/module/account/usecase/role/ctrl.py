from typing import Optional

from django.http import HttpRequest
from module.account.const import ProfileType
from module.account.service import AccountService
from module.account.usecase.role.logic import RoleLogic
from module.account.usecase.role.presenter import RolePagingPresent, RolePresent
from module.account.usecase.role.service import RoleService
from module.account.usecase.role.validator import CreateRoleInput, UpdateRoleInput
from ninja import Field, FilterSchema, Query, Router
from type.result import ErrorResponse, ErrorValue
from util.framework.authorization.auth_rbac import AuthRbac
from util.request_util import RequestUtil

router = Router()

MODULE = "role"
TAGS = ["account / manage role"]


class Filter(FilterSchema):
    q: Optional[str] = Field(None, q=["title__icontains"])


@router.get(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "get_list", [ProfileType.STAFF]),
    response={200: RolePagingPresent, 400: ErrorValue},
)
def get_list(
    request: HttpRequest, page: int = 1, order: str = "-id", filter: Filter = Query(...)
) -> RolePagingPresent | ErrorResponse:
    user = request.user
    role_service = RoleService()
    result, ok = RoleLogic.get_list_paging_role(role_service)(order, filter)
    if not ok:
        return RequestUtil.err(result)
    pem_option = RoleService().get_pem_option()
    profile_type_option = RoleService().get_profile_type_option(user.tenant_id)
    return RolePagingPresent.get_paging(page)(
        result, {"option": {"pem": pem_option, "profile_type": profile_type_option}}
    )


@router.get(
    "/{id}",
    tags=TAGS,
    auth=AuthRbac(MODULE, "get_item", [ProfileType.STAFF]),
    response={200: RolePresent, 400: ErrorValue},
)
def get_item(request: HttpRequest, id: int) -> RolePresent | ErrorResponse:
    account_service = AccountService()
    result, ok = RoleLogic.get_role(account_service)(id)
    return result if ok else RequestUtil.err(result)


@router.post(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "create", [ProfileType.STAFF]),
    response={200: RolePresent, 400: ErrorValue},
)
def create(request: HttpRequest, data: CreateRoleInput) -> RolePresent | ErrorResponse:
    account_service = AccountService()
    result, ok = RoleLogic.create_role(account_service)(data.dict())
    return result if ok else RequestUtil.err(result)


@router.put(
    "/{id}",
    tags=TAGS,
    auth=AuthRbac(MODULE, "update", [ProfileType.STAFF]),
    response={200: RolePresent, 400: ErrorValue},
)
def update(
    request: HttpRequest, id: int, data: UpdateRoleInput
) -> RolePresent | ErrorResponse:
    account_service = AccountService()
    result, ok = RoleLogic.update_role(account_service)(
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
    account_service = AccountService()
    result, ok = RoleLogic.delete_role(account_service)(id)
    return result if ok else RequestUtil.err(result)


@router.delete(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "delete_list", [ProfileType.STAFF]),
    response={200: list[int], 400: ErrorValue},
)
def delete_list(request: HttpRequest, ids: str) -> list[int] | ErrorResponse:
    id_list = ids.split(",")
    account_service = AccountService()
    result, ok = RoleLogic.delete_list_role(account_service)(id_list)
    return result if ok else RequestUtil.err(result)
