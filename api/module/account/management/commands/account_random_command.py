from django.core.management.base import BaseCommand
from type.general import Args, Kwargs


class Command(BaseCommand):
    help = "account_random_command"

    def handle(self, *args: Args, **options: Kwargs) -> None:
        self.stdout.write(self.style.SUCCESS("Start..."))
        self.stdout.write(self.style.SUCCESS("Done!!!"))
