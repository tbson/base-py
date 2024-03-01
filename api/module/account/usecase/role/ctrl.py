from typing import Optional

from django.http import HttpRequest
from module.account.const import ProfileType
from module.account.repo import AccountRepo
from module.account.usecase.role.service import RoleService
from module.account.usecase.role.presenter import RolePagingPresent, RolePresent
from module.account.usecase.role.repo import RoleRepo
from module.account.usecase.role.validator import CreateRoleInput, UpdateRoleInput
from ninja import Field, FilterSchema, Query, Router
from contract.type.result import ErrorResponse, ErrorValue
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
    result, ok = RoleService.get_list_paging_role(RoleRepo())(order, filter)
    if not ok:
        return RequestUtil.err(result)
    pem_option = RoleRepo().get_pem_option()
    profile_type_option = RoleRepo().get_profile_type_option(user.tenant_id)
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
    result, ok = RoleService.get_role(AccountRepo())(id)
    return result if ok else RequestUtil.err(result)


@router.post(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "create", [ProfileType.STAFF]),
    response={200: RolePresent, 400: ErrorValue},
)
def create(request: HttpRequest, data: CreateRoleInput) -> RolePresent | ErrorResponse:
    result, ok = RoleService.create_role(AccountRepo())(data.dict())
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
    result, ok = RoleService.update_role(AccountRepo())(
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
    result, ok = RoleService.delete_role(AccountRepo())(id)
    return result if ok else RequestUtil.err(result)


@router.delete(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "delete_list", [ProfileType.STAFF]),
    response={200: list[int], 400: ErrorValue},
)
def delete_list(request: HttpRequest, ids: str) -> list[int] | ErrorResponse:
    id_list = ids.split(",")
    result, ok = RoleService.delete_list_role(AccountRepo())(id_list)
    return result if ok else RequestUtil.err(result)
