from typing import Callable
from django.http import HttpRequest


class Cors:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpRequest:
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        return response
