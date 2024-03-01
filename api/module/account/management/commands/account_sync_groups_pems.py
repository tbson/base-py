from django.core.management.base import BaseCommand
from module.account.service import AccountService
from module.account.sync_groups_pems import AccountSyncGroupsPems
from module.account.usecase.account_command.logic import AccountCommandLogic
from type.general import Args, Kwargs


class Command(BaseCommand):
    help = "cmd_sync_all_pem"

    def handle(self, *args: Args, **options: Kwargs) -> None:
        self.stdout.write(self.style.SUCCESS("Start..."))
        AccountCommandLogic.sync_groups_pems(
            AccountService(), AccountSyncGroupsPems()
        )()
        self.stdout.write(self.style.SUCCESS("Done!!!"))
