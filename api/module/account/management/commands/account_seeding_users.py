from django.core.management.base import BaseCommand
from module.account.service import AccountService
from module.account.sync_role_service import AccountSyncRoleService
from module.account.usecase.account_command.logic import AccountCommandLogic
from module.account.usecase.account_command.service import AccountCommandService
from type.general import Args, Kwargs


class Command(BaseCommand):
    help = "cmd_account_seeding"

    def handle(self, *args: Args, **options: Kwargs) -> None:
        self.stdout.write(self.style.SUCCESS("Start..."))
        AccountCommandLogic.seeding_users(
            AccountService(), AccountSyncRoleService(), AccountCommandService()
        )()
        self.stdout.write(self.style.SUCCESS("Done!!!"))
