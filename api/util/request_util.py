from urllib.parse import parse_qs, urlsplit

from django.conf import settings
from type.result import ErrorResponse, ErrorValue


class RequestUtil:
    @staticmethod
    def err(error: ErrorValue, status_code: int = 400) -> ErrorResponse:
        return status_code, error

    @staticmethod
    def error_response_to_string(error_response: dict) -> list:
        result = []
        for _status, value in error_response.items():
            if isinstance(value, str) and value:
                result.append(value)
            if isinstance(value, list) and value:
                result += value
        return result

    @staticmethod
    def get_base_url() -> str:
        return f"{settings.PROTOCOL}://{settings.DOMAIN}/"

    @staticmethod
    def get_token(headers: dict) -> str:
        return headers.get("HTTP_AUTHORIZATION", "").split(" ")[-1]

    @staticmethod
    def get_lang_code(headers: dict) -> str:
        lang_code = headers.get("HTTP_ACCEPT_LANGUAGE", settings.LANGUAGE_CODE)
        if lang_code not in ["en-us", "vi-vn"]:
            lang_code = settings.LANGUAGE_CODE
        return lang_code

    @staticmethod
    def get_ips(headers: dict) -> list[str]:
        local_ip = "127.0.0.1"
        ip_str = headers.get("HTTP_X_FORWARDED_FOR", "")
        ips = [x.strip() for x in ip_str.split(",")] or [local_ip]
        if len(ips) == 1 and not ips[0]:
            ips = [local_ip]
        return ips

    @staticmethod
    def get_query_params(full_path: str) -> dict[str, str]:
        query = parse_qs(urlsplit(full_path).query)
        return {k: v[0] for k, v in query.items()}
