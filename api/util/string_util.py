import math
import random
import uuid

from django.utils.text import slugify


class StringUtil:
    @staticmethod
    def get_uuid() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def remove_special_chars(input_str: str, upper: bool = False) -> str:
        result = slugify(input_str).replace("-", "").strip()
        return result.upper() if upper else result

    @staticmethod
    def str_to_uid(input_str: str, upper: bool = False) -> str:
        result = slugify(input_str).replace("-", "_").strip()
        return result.upper() if upper else result

    @staticmethod
    def get_random_digits(string_length: int = 6) -> str:
        letters = "0123456789"
        return "".join(random.choice(letters) for _ in range(string_length))

    @staticmethod
    def ensure_space_slash(input_str: str) -> str:
        return input_str.replace("/", " / ").replace("  ", " ")

    @staticmethod
    def mask_prefix(input: str, mask_length: int = 4) -> str:
        remain = input[-mask_length:]
        prefix = "*" * (len(input) - mask_length)
        return f"{prefix}{remain}"

    @staticmethod
    def mask_email(email: str) -> str:
        email_arr = email.split("@")
        suffix = email_arr[1]
        name = email_arr[0]
        length = len(name)

        if length == 1:
            return f"*@{suffix}"

        mask_length = math.ceil(length / 2) if length <= 4 else 4
        name = StringUtil.mask_prefix(name, mask_length)

        return f"{name}@{suffix}"

    @staticmethod
    def apply_mask(input_str: str) -> str:
        if "@" in input_str:
            return StringUtil.mask_email(input_str)
        return StringUtil.mask_prefix(input_str)
