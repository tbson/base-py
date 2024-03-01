class OtpType:
    SIGNUP = 1
    RESET_PWD = 2


class OtpSource:
    EMAIL = 1
    MOBILE = 2


OTP_TYPE_CHOICE = (
    (OtpType.SIGNUP, "Signup"),
    (OtpType.RESET_PWD, "Reset password"),
)

OTP_SOURCE_CHOICE = (
    (OtpSource.EMAIL, "Email"),
    (OtpSource.MOBILE, "Mobile"),
)

OTP_TYPE_DICT = dict(OTP_TYPE_CHOICE)

OTP_SOURCE_DICT = dict(OTP_SOURCE_CHOICE)
