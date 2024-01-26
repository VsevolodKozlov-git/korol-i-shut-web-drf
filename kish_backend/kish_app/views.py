from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from kish_app import models, filters
import collections


class WordCloudAllApiView(APIView):
    def get(self, request):
        with open(settings.BASE_DIR/'data'/'svg', encoding='utf-8') as f:
            svg = ' '.join(f.readlines())

        return Response({'svg': svg}, status=status.HTTP_200_OK)


class GetWordFreq(APIView):
    """
    View возвращает сколько раз встречались слова
    Фильтры:
        - год начала/окончания year_min, year_max
        - Тип: ['all', 'nouns', 'verbs', 'adjectives']
    """

    def get(self, request):
        # tag_type filter
        url = request.get_full_path()
        possible_tags = ['all', 'nouns', 'verbs', 'adjectives']
        tag_type = request.query_params.get('tag_type')
        if tag_type is None:
            return Response({'errors': [{
                'type': "get_parameter_error",
                "detail": 'not provided tag_type in get request parameters',
                'instance': url
            }]}, status=status.HTTP_400_BAD_REQUEST)
        if tag_type not in possible_tags:
            return Response({'errors': [{
                'type': "get_parameter_error",
                "detail": "tag type should be one of the following ['all', 'nouns', 'verbs', 'adjectives']",
                'instance': url
            }]}, status=status.HTTP_400_BAD_REQUEST)
        if tag_type == 'all':
            tag_type = 'tokens'

        # year_filter
        albums = filters.FilterAlbumsByYear(request.GET).qs
        # get songs
        albums.prefetch_related('songs')
        all_songs = []
        for album in albums:
            album_songs = album.songs.all()
            all_songs.extend(album_songs)
        # get word frequency
        word_frequency_dict = self.get_word_freq(tag_type, all_songs)
        return Response(word_frequency_dict, status=200)


    @staticmethod
    def get_word_freq(tag_type, songs):
        words = [word for song in songs
                 for word in getattr(song, tag_type)]
        return collections.Counter(words)





class GetWordColor(APIView):
    """
    Возвращает словарь, где каждому слову соответсвтует его цвет в палитре rgb
    """

# Create your views here.
