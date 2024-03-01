from django.conf import settings
from django.test import TestCase
from module.account.repo import AccountRepo
from module.account.sync_role_repo import AccountSyncRoleRepo
from module.account.usecase.account_command.service import AccountCommandService
from module.account.usecase.account_command.repo import AccountCommandRepo
from module.auth.repo import AuthRepo
from module.auth.usecase.basic_auth.service import BasicAuthService
from module.auth.usecase.basic_auth.repo import BasicAuthRepo
from module.log.repo import LogRepo


class TestChangePwd(TestCase):
    def setUp(self) -> None:
        self.email = "admin@localhost"
        self.current_pwd = settings.SAMPLE_PASSWORD
        self.password = "12345678"
        self.password_confirm = "12345678"
        self.change_pwd = BasicAuthService.change_pwd(BasicAuthRepo(), LogRepo())
        self.login = BasicAuthService.login(AuthRepo(), BasicAuthRepo(), LogRepo())
        AccountCommandService.seeding_users(
            AccountRepo(), AccountSyncRoleRepo(), AccountCommandRepo()
        )()
        user, _ = AccountRepo().get_user(dict(email=self.email))
        self.user = user

    def test_happy_case(self) -> None:
        # login with current password
        _result, ok = self.login(self.email, self.current_pwd)
        self.assertTrue(ok)
        # change password
        result, ok = self.change_pwd(
            self.user, self.current_pwd, self.password, self.password_confirm
        )
        self.assertTrue(ok)

        # login with new password
        _result, ok = self.login(self.email, self.password)
        self.assertTrue(ok)

    def test_wrong_current_password(self) -> None:
        current_pwd = "wrong_password"
        result, ok = self.change_pwd(
            self.user, current_pwd, self.password, self.password_confirm
        )
        msg = {"detail": ["incorrect current password"]}
        self.assertEqual(result, msg)
        self.assertFalse(ok)
