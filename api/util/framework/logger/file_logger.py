from typing import Any
import contextlib
import inspect
import logging

from django.conf import settings


class FileLogger:
    @staticmethod
    def get_user(stack: Any) -> None:
        if "/views/" in stack.filename:
            with contextlib.suppress(Exception):
                request = stack[0].f_locals["request"]
                return request.user
        return None

    @staticmethod
    def log(content: Any, log_type: str = "debug") -> None:
        from util.date_util import DateUtil

        if log_type not in settings.LOG_TYPES:
            return
        LOGGER = logging.getLogger(f"custom_{log_type}")
        stacks = inspect.stack()
        files = []
        user = None
        try:
            for stack in stacks:
                if stored_user := FileLogger.get_user(stack):
                    user = stored_user

                if (
                    "/python3" not in stack.filename
                    and "/file_logger.py" not in stack.filename
                    and "/middleware/" not in stack.filename
                ):
                    files.append(f"{stack.filename}:{stack.lineno}")

            files.reverse()
            file = f"* {DateUtil.now()} - \"{user}\" - {', '.join(files)}"

            LOGGER.debug(file)
            LOGGER.debug(str(content))
        except Exception as e:  # skipcq: whatever error
            print(repr(e))
