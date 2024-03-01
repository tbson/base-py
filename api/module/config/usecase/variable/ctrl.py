from typing import Optional

from django.http import HttpRequest
from module.account.const import ProfileType
from module.config.repo import ConfigRepo
from module.config.usecase.variable.service import VariableService
from module.config.usecase.variable.presenter import (
    VariablePagingPresent,
    VariablePresent,
)
from module.config.usecase.variable.repo import VariableRepo
from module.config.usecase.variable.validator import (
    CreateVariableInput,
    UpdateVariableInput,
)
from ninja import Field, FilterSchema, Query, Router
from contract.type.result import ErrorResponse, ErrorValue
from util.framework.authorization.auth_rbac import AuthRbac
from util.request_util import RequestUtil

router = Router()

MODULE = "variable"
TAGS = ["config / manage variable"]


class Filter(FilterSchema):
    type: Optional[int] = None
    q: Optional[str] = Field(
        None, q=["uid__icontains", "value__icontains", "description__icontains"]
    )


@router.get(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "get_list", [ProfileType.STAFF]),
    response={200: VariablePagingPresent, 400: ErrorValue},
)
def get_list(
    request: HttpRequest, page: int = 1, order: str = "-id", filter: Filter = Query(...)
) -> VariablePagingPresent | ErrorResponse:
    result, ok = VariableService.get_list_paging_variable(VariableRepo())(order, filter)
    if not ok:
        return RequestUtil.err(result)
    type_option = VariableRepo().get_type_option()
    return VariablePagingPresent.get_paging(page)(
        result, {"option": {"type": type_option}}
    )


@router.get(
    "/{id}",
    tags=TAGS,
    auth=AuthRbac(MODULE, "get_item", [ProfileType.STAFF]),
    response={200: VariablePresent, 400: ErrorValue},
)
def get_item(request: HttpRequest, id: int) -> VariablePresent | ErrorResponse:
    result, ok = VariableService.get_variable(ConfigRepo())(id)
    return result if ok else RequestUtil.err(result)


@router.post(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "create", [ProfileType.STAFF]),
    response={200: VariablePresent, 400: ErrorValue},
)
def create(
    request: HttpRequest, data: CreateVariableInput
) -> VariablePresent | ErrorResponse:
    result, ok = VariableService.create_variable(ConfigRepo())(data.dict())
    return result if ok else RequestUtil.err(result)


@router.put(
    "/{id}",
    tags=TAGS,
    auth=AuthRbac(MODULE, "update", [ProfileType.STAFF]),
    response={200: VariablePresent, 400: ErrorValue},
)
def update(
    request: HttpRequest, id: int, data: UpdateVariableInput
) -> VariablePresent | ErrorResponse:
    result, ok = VariableService.update_variable(ConfigRepo())(
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
    result, ok = VariableService.delete_variable(ConfigRepo())(id)
    return result if ok else RequestUtil.err(result)


@router.delete(
    "/",
    tags=TAGS,
    auth=AuthRbac(MODULE, "delete_list", [ProfileType.STAFF]),
    response={200: list[int], 400: ErrorValue},
)
def delete_list(request: HttpRequest, ids: str) -> list[int] | ErrorResponse:
    id_list = ids.split(",")
    result, ok = VariableService.delete_list_variable(ConfigRepo())(id_list)
    return result if ok else RequestUtil.err(result)
