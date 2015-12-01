from django.core.management.base import BaseCommand, CommandError
from src.models import History, Wines


class Command(BaseCommand):
    help = 'Harvests the wine from JoshLikesWine.com'

    def handle(self, *args, **options):
        self.stdout.write('Harvested')
