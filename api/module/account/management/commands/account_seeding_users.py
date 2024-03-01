from django.core.management.base import BaseCommand
from module.account.repo import AccountRepo
from module.account.sync_role_repo import AccountSyncRoleRepo
from module.account.usecase.account_command.service import AccountCommandService
from module.account.usecase.account_command.repo import AccountCommandRepo
from contract.type.general import Args, Kwargs


class Command(BaseCommand):
    help = "cmd_account_seeding"

    def handle(self, *args: Args, **options: Kwargs) -> None:
        self.stdout.write(self.style.SUCCESS("Start..."))
        AccountCommandService.seeding_users(
            AccountRepo(), AccountSyncRoleRepo(), AccountCommandRepo()
        )()
        self.stdout.write(self.style.SUCCESS("Done!!!"))
