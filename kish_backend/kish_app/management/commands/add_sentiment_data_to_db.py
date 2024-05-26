from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from django.conf import settings
from kish_app import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        data_dir = settings.BASE_DIR / 'data'
        df = pd.read_csv(data_dir / 'kish_sentiment.csv')
        for ind, row in df.iterrows():
            album_id = row['album_id'] + 1

            title = row['title']
            songs = models.Song.objects.filter(album__pk=album_id, title=title)
            if len(songs) > 1:
                raise CommandError(
                    f'Для title: {title}, album_id: {album_id} больше 1-й песни'
                )
            song = songs[0]
            song.positive = row['positive']
            song.negative = row['negative']
            song.neutral = row['neutral']
            song.save()
