from django.conf import settings
from django.test import TestCase
from contract.interface.email import Email
from module.account.repo import AccountRepo
from module.account.sync_role_repo import AccountSyncRoleRepo
from module.account.usecase.account_command.service import AccountCommandService
from module.account.usecase.account_command.repo import AccountCommandRepo
from module.auth.repo import AuthRepo
from module.auth.usecase.basic_auth.service import BasicAuthService
from module.auth.usecase.basic_auth.repo import BasicAuthRepo
from module.log.repo import LogRepo
from module.verify.const import OtpType
from module.verify.repo import VerifyRepo
from module.verify.usecase.otp.service import OtpService
from contract.type.email import EmailBody, EmailSubject, EmailTo
from util.string_util import StringUtil


class EmailRepo(Email):
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
        self.reset_pwd = BasicAuthService.reset_pwd(
            BasicAuthRepo(), AccountRepo(), VerifyRepo(), LogRepo()
        )
        self.send_otp = OtpService.send_otp(AccountRepo(), VerifyRepo(), EmailRepo())
        self.login = BasicAuthService.login(AuthRepo(), BasicAuthRepo(), LogRepo())

        AccountCommandService.seeding_users(
            AccountRepo(), AccountSyncRoleRepo(), AccountCommandRepo()
        )()

        VerifyRepo().set_trusted_target(self.username)

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
