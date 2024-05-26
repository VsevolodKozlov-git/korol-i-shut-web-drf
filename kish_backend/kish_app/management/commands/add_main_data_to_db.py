from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from django.conf import settings
from kish_app import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        data_dir = settings.BASE_DIR / 'data'

        print('adding albums in db')
        df_album = pd.read_csv(data_dir / 'kish_albums.csv')
        id_album_dict = {}
        for ind, row in df_album.iterrows():
            album_id = row['album_id']

            del row['album_id']  # no column album_id in model
            album_obj = models.Album(**row)
            id_album_dict[album_id] = album_obj
            album_obj.save()

        print('adding songs in db')
        df_song = pd.read_pickle(data_dir / 'songs_tagged.pkl')
        for ind, row in df_song.iterrows():
            album_id = row['album_id']
            # no column album_id in model
            del row['album_id']
            album = id_album_dict[album_id]
            row['album'] = album
            song_obj = models.Song(**row)
            song_obj.save()

        print('adding word ratings in db')
        df_word_rating = pd.read_csv(data_dir / 'kish_word_rating.csv')
        for ind, row in df_word_rating.iterrows():
            word_rating_obj = models.WordRating(**row)
            word_rating_obj.save()
