from django.core.management.base import BaseCommand
from core.models import Customer

from sqlalchemy import create_engine
from sqlalchemy import text

sqlite_engine = create_engine("sqlite+pysqlite:///manolibakes/db.sqlite3")


class Command(BaseCommand):
    help = "Migrate data from sqlite to postgres"

    def handle(self, *args, **options):
        query = text("SELECT * FROM core_customer")
        with sqlite_engine.connect() as conn:
            for customer in conn.execute(query):
                customer_model = Customer(*customer)
                customer_model.save()
