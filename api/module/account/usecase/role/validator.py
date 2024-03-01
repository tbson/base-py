from typing import Optional

from ninja import Schema


class CreateRoleInput(Schema):
    key: str
    value: str
    description: str = ""
    type: int
    pem_ids: list[int]


class UpdateRoleInput(Schema):
    key: Optional[str]
    value: Optional[str]
    description: Optional[str]
    type: Optional[int]
    pem_ids: Optional[list[int]]
