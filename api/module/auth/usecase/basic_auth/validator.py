from ninja import Field, Schema


class LoginInput(Schema):
    username: str = Field(min_length=2, max_length=64)
    password: str


class ChangePwdInput(Schema):
    current_password: str
    password: str = Field(min_length=8, max_length=64)
    password_confirm: str


class RequestResetPwdInput(Schema):
    username: str = Field(min_length=2, max_length=64)


class ResetPwdInput(Schema):
    username: str
    verify_id: str
    verify_code: str
    password: str = Field(min_length=8, max_length=64)
    password_confirm: str
