from typing import Callable, cast

from interface.account import Account
from interface.email import Email
from interface.verify import Verify
from ninja import Schema
from type.result import Result
from type.schema import OtpSchema, UserSchema
from util.date_util import DateUtil
from util.string_util import StringUtil


class SendOtpOutput(Schema):
    verify_id: str
    verify_target: str


class OtpLogic:
    @staticmethod
    def send_otp(
        account_service: Account, verify_service: Verify, email_service: Email
    ) -> Callable:
        def inner(
            username: str, otp_type: int, ips: list[str]
        ) -> Result[SendOtpOutput]:
            default_result = SendOtpOutput(
                verify_id=StringUtil.get_uuid(),
                verify_target=StringUtil.apply_mask(username),
            )
            (user, ok) = account_service.get_user(dict(username=username))
            if not ok:
                return default_result, True
            user = cast(UserSchema, user)
            email = user.email
            (result, ok) = verify_service.create_otp(email, otp_type, ips)
            if not ok:
                return result, False
            otp = cast(OtpSchema, result)
            # Do not send email to trusted target
            if not verify_service.is_trusted_target(email):
                (subject, body, to) = verify_service.get_otp_email_input(otp)
                email_service.send_email_async(subject, body, to)
            return (
                SendOtpOutput(
                    verify_id=str(otp.id),
                    verify_target=StringUtil.apply_mask(email),
                ),
                True,
            )

        return inner

    @staticmethod
    def verify_otp(verify_service: Verify) -> Callable[[str, str], Result[OtpSchema]]:
        def inner(verify_id: str, verify_code: str) -> Result[OtpSchema]:
            return verify_service.verify_otp(verify_id, verify_code)

        return inner

    @staticmethod
    def check_otp(verify_service: Verify) -> Callable[[str, str], Result[OtpSchema]]:
        def inner(verify_id: str, verify_code: str) -> Result[OtpSchema]:
            return verify_service.verify_otp(verify_id, verify_code, True)

        return inner

    @staticmethod
    def resend_otp(
        account_service: Account, verify_service: Verify, email_service: Email
    ) -> Callable[[str], Result[SendOtpOutput]]:
        def inner(id: str) -> Result[SendOtpOutput]:
            result, ok = verify_service.get_otp(
                dict(id=id, resend_expired_at__gte=DateUtil.now())
            )
            if not ok:
                return result, False
            otp = cast(OtpSchema, result)

            target = otp.target
            otp_type = otp.type
            ips = otp.ips

            return OtpLogic.send_otp(account_service, verify_service, email_service)(
                target, otp_type, ips
            )

        return inner
