from typing import Optional

from django.http import HttpRequest
from module.account.service import AccountService
from ninja.security import HttpBearer
from util.framework.authorization.auth_bearer import check_authenticate

pem_list = []


class AuthRbac(HttpBearer):
    def __init__(self, module: str, action: str, profile_types: list[int]) -> None:
        self.module = module
        self.action = action
        pem_list.append((module, action, profile_types))

    def authenticate(self, request: HttpRequest, token: str) -> Optional[str]:
        if not check_authenticate(request, token):
            return None
        if request.user.is_staff or request.user.is_superuser:
            return token
        account_service = AccountService()
        pems, ok = account_service.get_list_pem(
            dict(module=self.module, action=self.action, roles__users=request.user)
        )
        if not ok:
            return None
        return token if len(list(pems)) else None


class AuthRbacUtil:
    @staticmethod
    def get_pem_list() -> list[tuple[str, str, list[int]]]:
        return pem_list
