from typing import Optional

from ninja import Schema


class CreateVariableInput(Schema):
    uid: str
    value: str
    description: str = ""
    type: int


class UpdateVariableInput(Schema):
    uid: Optional[str]
    value: Optional[str]
    description: Optional[str]
    type: Optional[int]
