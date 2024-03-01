from typing import Optional

from ninja import Schema


class CreateUserInput(Schema):
    email: str
    mobile: Optional[str]
    first_name: str
    last_name: str
    password: str
    role_ids: list[int]


class UpdateUserInput(Schema):
    email: Optional[str]
    mobile: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    role_ids: Optional[list[int]]
