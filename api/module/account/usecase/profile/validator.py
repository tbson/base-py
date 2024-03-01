from typing import Optional

from ninja import Schema


class UpdateProfileInput(Schema):
    first_name: str
    last_name: str
    mobile: Optional[str]
