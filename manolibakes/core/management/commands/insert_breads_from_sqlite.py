from django.core.management.base import BaseCommand
from core.models import Bread

from sqlalchemy import create_engine
from sqlalchemy import text

sqlite_engine = create_engine("sqlite+pysqlite:///manolibakes/db.sqlite3")


class Command(BaseCommand):
    help = "Migrate data from sqlite to postgres"

    def handle(self, *args, **options):
        query = text("SELECT * FROM core_bread")
        with sqlite_engine.connect() as conn:
            for bread in conn.execute(query):
                bread_model = Bread(*bread)
                bread_model.save()
