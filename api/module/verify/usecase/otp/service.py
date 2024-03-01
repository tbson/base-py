from typing import Callable, cast

from contract.interface.account import Account
from contract.interface.email import Email
from contract.interface.verify import Verify
from ninja import Schema
from contract.type.result import Result
from contract.type.schema import OtpSchema, UserSchema
from util.date_util import DateUtil
from util.string_util import StringUtil


class SendOtpOutput(Schema):
    verify_id: str
    verify_target: str


class OtpService:
    @staticmethod
    def send_otp(
        account_repo: Account, verify_repo: Verify, email_repo: Email
    ) -> Callable:
        def inner(
            username: str, otp_type: int, ips: list[str]
        ) -> Result[SendOtpOutput]:
            default_result = SendOtpOutput(
                verify_id=StringUtil.get_uuid(),
                verify_target=StringUtil.apply_mask(username),
            )
            (user, ok) = account_repo.get_user(dict(username=username))
            if not ok:
                return default_result, True
            user = cast(UserSchema, user)
            email = user.email
            (result, ok) = verify_repo.create_otp(email, otp_type, ips)
            if not ok:
                return result, False
            otp = cast(OtpSchema, result)
            # Do not send email to trusted target
            if not verify_repo.is_trusted_target(email):
                (subject, body, to) = verify_repo.get_otp_email_input(otp)
                email_repo.send_email_async(subject, body, to)
            return (
                SendOtpOutput(
                    verify_id=str(otp.id),
                    verify_target=StringUtil.apply_mask(email),
                ),
                True,
            )

        return inner

    @staticmethod
    def verify_otp(verify_repo: Verify) -> Callable[[str, str], Result[OtpSchema]]:
        def inner(verify_id: str, verify_code: str) -> Result[OtpSchema]:
            return verify_repo.verify_otp(verify_id, verify_code)

        return inner

    @staticmethod
    def check_otp(verify_repo: Verify) -> Callable[[str, str], Result[OtpSchema]]:
        def inner(verify_id: str, verify_code: str) -> Result[OtpSchema]:
            return verify_repo.verify_otp(verify_id, verify_code, True)

        return inner

    @staticmethod
    def resend_otp(
        account_repo: Account, verify_repo: Verify, email_repo: Email
    ) -> Callable[[str], Result[SendOtpOutput]]:
        def inner(id: str) -> Result[SendOtpOutput]:
            result, ok = verify_repo.get_otp(
                dict(id=id, resend_expired_at__gte=DateUtil.now())
            )
            if not ok:
                return result, False
            otp = cast(OtpSchema, result)

            target = otp.target
            otp_type = otp.type
            ips = otp.ips

            return OtpService.send_otp(account_repo, verify_repo, email_repo)(
                target, otp_type, ips
            )

        return inner
