from django.conf import settings
from django.test import TestCase
from interface.email import Email
from module.account.service import AccountService
from module.account.sync_role_service import AccountSyncRoleService
from module.account.usecase.account_command.logic import AccountCommandLogic
from module.account.usecase.account_command.service import AccountCommandService
from module.auth.service import AuthService
from module.auth.usecase.basic_auth.logic import BasicAuthLogic
from module.auth.usecase.basic_auth.service import BasicAuthService
from module.log.service import LogService
from module.verify.const import OtpType
from module.verify.service import VerifyService
from module.verify.usecase.otp.logic import OtpLogic
from type.email import EmailBody, EmailSubject, EmailTo
from util.string_util import StringUtil


class EmailService(Email):
    def send_email_async(
        self, subject: EmailSubject, body: EmailBody, to: EmailTo
    ) -> None:
        return None


class TestResetPwd(TestCase):
    def setUp(self) -> None:
        self.username = "admin@localhost"
        self.ips = ["127.0.0.1"]
        self.password = settings.SAMPLE_PASSWORD
        self.new_password = f"{settings.SAMPLE_PASSWORD}1"
        self.new_password_confirm = f"{settings.SAMPLE_PASSWORD}1"
        self.new_password_wrong_confirm = f"{settings.SAMPLE_PASSWORD}2"
        self.reset_pwd = BasicAuthLogic.reset_pwd(
            BasicAuthService(), AccountService(), VerifyService(), LogService()
        )
        self.send_otp = OtpLogic.send_otp(
            AccountService(), VerifyService(), EmailService()
        )
        self.login = BasicAuthLogic.login(
            AuthService(), BasicAuthService(), LogService()
        )

        AccountCommandLogic.seeding_users(
            AccountService(), AccountSyncRoleService(), AccountCommandService()
        )()

        VerifyService().set_trusted_target(self.username)

    def test_happy_case(self) -> None:
        result, ok = self.send_otp(self.username, OtpType.RESET_PWD, self.ips)
        self.assertTrue(ok)

        verify_id = result.verify_id
        verify_code = settings.OTP_TRUSTED_CODE

        result, ok = self.reset_pwd(
            self.username,
            verify_id,
            verify_code,
            self.new_password,
            self.new_password_confirm,
        )
        self.assertTrue(ok)

        result, ok = self.login(self.username, self.new_password)
        self.assertTrue(ok)

    def test_wrong_verify_id(self) -> None:
        verify_id = StringUtil.get_uuid()
        verify_code = settings.OTP_TRUSTED_CODE
        result, ok = self.reset_pwd(
            self.username,
            verify_id,
            verify_code,
            self.new_password,
            self.new_password_confirm,
        )
        self.assertFalse(ok)

    def test_wrong_verify_code(self) -> None:
        result, _ok = self.send_otp(self.username, OtpType.RESET_PWD, self.ips)

        verify_id = result.verify_id
        verify_code = "wrong"

        result, ok = self.reset_pwd(
            self.username,
            verify_id,
            verify_code,
            self.new_password,
            self.new_password_confirm,
        )
        self.assertFalse(ok)

    def test_mismatch_password_confirm(self) -> None:
        result, _ok = self.send_otp(self.username, OtpType.RESET_PWD, self.ips)

        verify_id = result.verify_id
        verify_code = settings.OTP_TRUSTED_CODE

        result, ok = self.reset_pwd(
            self.username,
            verify_id,
            verify_code,
            self.new_password,
            self.new_password_wrong_confirm,
        )
        self.assertFalse(ok)
