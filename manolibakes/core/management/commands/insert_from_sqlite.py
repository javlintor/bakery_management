from django.core.management.base import BaseCommand
import logging
from core.models import Bread, Customer

from sqlalchemy import create_engine
from sqlalchemy import text

sqlite_engine = create_engine("sqlite+pysqlite:///data/db.sqlite3")


class Command(BaseCommand):
    help = "Migrate data from sqlite to postgres"

    def handle(self, *args, **options):
        with sqlite_engine.connect() as conn:
            try:
                query = text("SELECT * FROM core_bread")
                for bread in conn.execute(query):
                    bread_model = Bread(*bread)
                    bread_model.save()
            except Exception as e:
                logging.error(f"Something went wrong when inserting bread: {e}")

            try:
                query = text("SELECT * FROM core_customer")
                for customer in conn.execute(query):
                    customer_model = Customer(*customer)
                    customer_model.save()
            except Exception as e:
                logging.error(f"Something went wrong when inserting customers: {e}")
