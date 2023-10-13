from django.core.management.base import BaseCommand

from core.models import Bread


class Command(BaseCommand):
    help = "Create and insert sample breads"

    def handle(self, *args, **options):
        new_breads = [
            Bread(name="Barra"),
            Bread(name="Mollete"),
            Bread(name="Rústica"),
            Bread(name="Hogaza"),
        ]
        for bread in new_breads:
            bread.save()
