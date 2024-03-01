from django.conf import settings
from django.test import TestCase
from module.account.service import AccountService
from module.account.sync_role_service import AccountSyncRoleService
from module.account.usecase.account_command.logic import AccountCommandLogic
from module.account.usecase.account_command.service import AccountCommandService
from module.auth.service import AuthService
from module.auth.usecase.basic_auth.logic import BasicAuthLogic
from module.auth.usecase.basic_auth.service import BasicAuthService
from module.log.service import LogService


class TestChangePwd(TestCase):
    def setUp(self) -> None:
        self.email = "admin@localhost"
        self.current_pwd = settings.SAMPLE_PASSWORD
        self.password = "12345678"
        self.password_confirm = "12345678"
        self.change_pwd = BasicAuthLogic.change_pwd(BasicAuthService(), LogService())
        self.login = BasicAuthLogic.login(
            AuthService(), BasicAuthService(), LogService()
        )
        AccountCommandLogic.seeding_users(
            AccountService(), AccountSyncRoleService(), AccountCommandService()
        )()
        user, _ = AccountService().get_user(dict(email=self.email))
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
