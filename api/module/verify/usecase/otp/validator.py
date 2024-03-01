from ninja import Schema


class SendOtpInput(Schema):
    username: str


class VerifyOtpInput(Schema):
    verify_id: str
    verify_code: str


class ResendOtpInput(Schema):
    verify_id: str
