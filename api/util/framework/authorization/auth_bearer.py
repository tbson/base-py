from typing import Union

from django.http import HttpRequest
from module.account.repo import AccountRepo
from ninja.security import HttpBearer
from util.token_util import TokenUtil


def check_authenticate(request: HttpRequest, token: str) -> Union[str, None]:
    if not TokenUtil.is_access(token):
        return None
    user_id = TokenUtil.get_id(token)
    account_repo = AccountRepo()
    result, ok = account_repo.get_user(dict(id=user_id))
    if not ok:
        return None
    request.user = result
    return token


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Union[str, None]:
        return check_authenticate(request, token)
