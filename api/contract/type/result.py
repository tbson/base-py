from typing import Dict, List, Literal, Tuple, TypeVar, Union

OkTag = Literal[True]
OktValue = TypeVar("OktValue")
OkResult = Tuple[OktValue, OkTag]

ErrorTag = Literal[False]
ErrorValue = Dict[str, List[str]]
ErrorResult = Tuple[ErrorValue, ErrorTag]
ErrorResponse = tuple[int, ErrorValue]

Result = Union[OkResult[OktValue], ErrorResult]
