from django.http import HttpRequest, JsonResponse
from module.account.usecase.profile.ctrl import router as profile_router
from module.account.usecase.role.ctrl import router as role_router
from module.account.usecase.user.ctrl import router as user_router
from module.auth.usecase.basic_auth.ctrl import router as basic_auth_router
from module.auth.usecase.common_auth.ctrl import router as common_auth_route
from module.config.usecase.variable.ctrl import router as variable_router
from module.verify.usecase.otp.ctrl import router as otp_router
from ninja import NinjaAPI
from ninja.errors import ValidationError
from util.error_util import ErrorUtil

api = NinjaAPI()


@api.exception_handler(ValidationError)
def validation_errors(request: HttpRequest, exc: ValidationError) -> JsonResponse:
    error = ErrorUtil.format(exc)
    return JsonResponse(error, status=400)


class RouteUtil:
    _routes: dict[str, list[int]] = {}

    @staticmethod
    def get_routes() -> list[tuple[str, NinjaAPI]]:
        return [
            ("/auth/basic-auth", basic_auth_router),
            ("/auth/common-auth", common_auth_route),
            ("/account/user", user_router),
            ("/account/profile", profile_router),
            ("/account/role", role_router),
            ("/verify/otp", otp_router),
            ("/config/variable", variable_router),
        ]

    @staticmethod
    def register_route() -> NinjaAPI:
        route_map = RouteUtil.get_routes()
        for prefix, router in route_map:
            api.add_router(prefix, router)
        return api

    @staticmethod
    def get_action_map() -> dict[str, list[int]]:
        return RouteUtil._routes
