from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from module.account.service import AccountService
from module.account.sync_role_service import AccountSyncRoleService
from module.account.usecase.account_command.logic import AccountCommandLogic
from module.account.usecase.account_command.service import AccountCommandService
from module.auth.service import AuthService
from module.auth.usecase.basic_auth.logic import BasicAuthLogic
from module.auth.usecase.basic_auth.service import BasicAuthService
from module.log.service import LogService

User = get_user_model()


class TestLogin(TestCase):
    def setUp(self) -> None:
        self.password = settings.SAMPLE_PASSWORD
        self.login = BasicAuthLogic.login(
            AuthService(), BasicAuthService(), LogService()
        )

        AccountCommandLogic.seeding_users(
            AccountService(), AccountSyncRoleService(), AccountCommandService()
        )()

    def test_happy_case(self) -> None:
        _result, ok = self.login("admin@localhost", self.password)
        self.assertTrue(ok)

    def test_wrong_credential(self) -> None:
        result, ok = self.login("tbson871@gmail.com", self.password)
        msg = {"detail": ["incorrect login information, please try again"]}
        self.assertFalse(ok)
        self.assertEqual(result, msg)

    def test_inactivated_user(self) -> None:
        user = User.objects.get(username="admin@localhost")
        user.is_active = False
        user.save()
        result, ok = self.login("admin@localhost", self.password)
        msg = {"detail": ["account is not active"]}
        self.assertFalse(ok)
        self.assertEqual(result, msg)
