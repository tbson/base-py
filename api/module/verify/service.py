from datetime import timedelta
from typing import Optional, cast

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from interface.verify import Verify
from module.verify.models import Otp, TrustedTarget
from type.general import Condition
from type.result import Result
from type.schema import OtpSchema
from util.date_util import DateUtil
from util.error_util import ErrorUtil
from util.string_util import StringUtil

ExtraData = Optional[dict[str, str]]

OTP_LENGTH = 6


class VerifyService(Verify):
    def get_otp(
        self, condition: Condition, for_resend: bool = False
    ) -> Result[OtpSchema]:
        try:
            if not for_resend:
                condition["expired_at__gte"] = DateUtil.now()
            condition["verified_at"] = None
            condition["fail_checks__lte"] = settings.OTP_MAX_FAIL_CHECKS
            otp = Otp.objects.get(**condition)
            return otp, True
        except Otp.DoesNotExist:
            err_msg = _("OTP does not exist")
            return ErrorUtil.format(err_msg), False

    def create_otp(
        self,
        target: str,
        otp_type: int,
        ips: list[str],
        extra_data: ExtraData = None,
    ) -> Result[OtpSchema]:
        if extra_data is None:
            extra_data = {}
        if not self.__is_allow_to_create_otp(target, ips):
            err_msg = _("OTP daily quota exceeded")
            return ErrorUtil.format(err_msg), False
        code = StringUtil.get_random_digits(OTP_LENGTH)
        if self.is_trusted_target(target):
            code = settings.OTP_TRUSTED_CODE
        try:
            now = DateUtil.now()
            data = {
                "target": target,
                "type": otp_type,
                "code": code,
                "ips": ips,
                "verified_at": None,
                "expired_at": now + timedelta(seconds=settings.OTP_LIFETIME),
                "resend_expired_at": now
                + timedelta(seconds=settings.OTP_RESEND_PERIOD),
                "extra_data": extra_data,
            }
            otp = Otp.objects.create(**data)
            return otp, True
        except Exception as e:
            print(e)
            err_msg = _("Failed to create OTP")
            return ErrorUtil.format(err_msg), False

    def verify_otp(
        self, verify_id: str, verify_code: str, for_checking: bool = False
    ) -> Result[OtpSchema]:
        try:
            result, ok = self.get_otp(dict(id=verify_id))
            if not ok:
                return result, False
            otp = cast(OtpSchema, result)
            if otp.code != verify_code:
                otp.fail_checks += 1
                otp.save()
                err_msg = _("OTP code is not valid")
                return ErrorUtil.format(err_msg), False
            if not for_checking:
                otp.verified_at = DateUtil.now()
                otp.save()
            return otp, True
        except Otp.DoesNotExist:
            err_msg = _("OTP does not exist or expired")
            return ErrorUtil.format(err_msg), False

    def is_trusted_target(self, target: str) -> bool:
        try:
            TrustedTarget.objects.get(target=target)
            return True
        except TrustedTarget.DoesNotExist:
            return False

    def set_trusted_target(self, target: str) -> Result[TrustedTarget]:
        trusted_target, _ = TrustedTarget.objects.get_or_create(target=target)
        return trusted_target, True

    def get_otp_email_input(self, otp: OtpSchema) -> tuple[str, str, str]:
        return (_("OTP Verification"), self.__get_otp_template(otp.code), otp.target)

    def __is_allow_to_create_otp(self, target: str, ips: list[str]) -> bool:
        quota_per_day = settings.OTP_QUOTA_PER_DAY
        today = DateUtil.today()
        quta = Otp.objects.filter(
            target=target, ips__contains=ips, created_at__date=today
        ).count()
        return quta <= quota_per_day

    def __get_otp_template(self, code: str) -> str:
        return f"""
            <div>
                <p>Dear sir/madam,</p>
                <p>
                    This is Your OTP code: <strong>{code}</strong>
                </p>
                <p>Please do not share this code.</p>
                <p>Sincerely</p>
            </div>
        """
