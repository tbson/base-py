# import sys
from typing import Any, Optional

from django.utils.translation import gettext_lazy as _
from ninja.errors import ValidationError
from type.result import ErrorValue

PYDANTIC_ERROR_MAP = {
    "value_error.missing": _("this field is required"),
    "value_error.any_str.max_length": _(
        "ensure this value has at most {limit_value} characters"
    ),
    "value_error.any_str.min_length": _(
        "ensure this value has at least {limit_value} characters"
    ),
    "value_error.number.not_gt": _("ensure this value is greater than {limit_value}"),
    "value_error.number.not_lt": _("ensure this value is greater than {limit_value}"),
}


class ErrorUtil:
    """
    @staticmethod
    def return_exception(e: Any) -> str:
        exc_tb = sys.exc_info()[2]
        file_name = exc_tb.tb_frame.f_code.co_filename
        return f"{str(e)} => {file_name}:{str(exc_tb.tb_lineno)}"
    """

    @staticmethod
    def format(data: Any) -> ErrorValue:
        # Instance of lazy translation
        if hasattr(data, "capitalize"):
            data = str(data)
        if isinstance(data, str):
            return {"detail": [data]}
        if hasattr(data, "detail"):
            data = data.detail
        if isinstance(data, ValidationError):

            def parse_msg(i: dict) -> list[str]:
                error_type = i["type"]
                raw_msg = PYDANTIC_ERROR_MAP.get(error_type)
                if not raw_msg:
                    return [i["msg"]]

                ctx = i.get("ctx", {})
                return [raw_msg.format(**ctx)]

            data = {".".join(i["loc"][2:]): parse_msg(i) for i in data.errors}
        return data if isinstance(data, dict) else {"detail": [str(data)]}

    @staticmethod
    def get_str(data: Optional[ErrorValue]) -> str:
        return str(data) if data else ""
