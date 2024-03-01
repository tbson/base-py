from ninja import Schema


class SendOtpOutput(Schema):
    verify_id: str
    verify_target: str
