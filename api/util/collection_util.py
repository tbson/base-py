import itertools
from typing import Any, List, Optional


class CollectionUtil:
    @staticmethod
    def convert_list_to_string(value: list[Any]) -> str:
        return ", ".join(value) if isinstance(value, list) else value

    @staticmethod
    def convert_string_to_list(str_value: str) -> list[str]:
        if isinstance(str_value, str):
            return [value.strip() for value in str_value.split(",")]
        return []

    @staticmethod
    def flat_2d_list(items: List[Any]) -> List[Any]:
        return list(set(itertools.chain.from_iterable(items)))

    @staticmethod
    def get_tuple_value(
        input_tuple: tuple[tuple[str, Any]],
        key: str,
        default_value: Optional[str] = None,
    ) -> Optional[str]:
        result_dict = dict(input_tuple)
        return result_dict.get(key, default_value)

    @staticmethod
    def is_boolean_dict(input_dict: dict) -> bool:
        return (
            all(isinstance(item, bool) for item in input_dict.values())
            if input_dict.values()
            else False
        )
