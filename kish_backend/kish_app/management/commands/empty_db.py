from django.core.management.base import BaseCommand, CommandError
from kish_app import models
from django.db import connection


class Command(BaseCommand):
    @staticmethod
    def empty_table(model):
        model.objects.all().delete()

    @staticmethod
    def reset_table_seq(model):
        sequence_name = model._meta.db_table + "_id_seq"
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1;")

    def handle(self, *args, **options):
        models_to_empty = [
            models.Song,
            models.WordRating,
            models.Album
        ]
        for model in models_to_empty:
            print(f'emptying {model}')
            self.empty_table(model)
            self.reset_table_seq(model)
        print('All tables emptied')