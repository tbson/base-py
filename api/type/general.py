from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional, Union

from django_hint import QueryType, StandardModelType

QuerySet = QueryType
QuerySetObj = StandardModelType
Args = Optional[Any]
Kwargs = Optional[Any]
Condition = Dict[
    str,
    Union[
        str,
        int,
        date,
        datetime,
        list[int],
        list[str],
        dict,
        float,
        bool,
        Literal[None],
    ],
]
Token = str
ProfileType = int
Permissions = Dict[str, List[str]]
IPs = List[str]
