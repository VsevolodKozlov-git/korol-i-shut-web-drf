from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.apps import apps

from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import HttpRequest

from rest_framework.request import Request
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from kish_app import models, filters, serializers
import collections



class WordCloudAllApiView(APIView):
    def get(self, request: Request):
        with open(settings.BASE_DIR/'data'/'svg', encoding='utf-8') as f:
            svg = ' '.join(f.readlines())

        return Response({'svg': svg}, status=status.HTTP_200_OK)


class WordFreqApiView(APIView):
    """
    View возвращает сколько раз встречались слова
    Фильтры:
        - год начала/окончания year_min, year_max
        - Тип: ['all', 'nouns', 'verbs', 'adjectives']
    """

    def get(self, request: Request):
        # tag_type handling
        tag_type_filter = filters.TagTypeFilter(request)
        if tag_type_filter.errors:
            return Response(tag_type_filter.errors, status=status.HTTP_400_BAD_REQUEST)
        tag_type = tag_type_filter.data
        # counting word frequency
        songs_qs = filters.FilterSongs(request.GET).qs
        word_freq_dict = self.get_word_freq(songs_qs, tag_type)
        # return
        return Response(word_freq_dict, status=200)


    @staticmethod
    def get_word_freq(songs_qs, tag_type):
        word_lists = songs_qs.values_list(tag_type, flat=True)
        words = [word for word_list in word_lists
                 for word in word_list]
        word_freq_dict = collections.Counter(words)
        return word_freq_dict


class WordColorApiView(APIView):
    """
    Возвращает словарь, где каждому слову соответсвтует его цвет в палитре rgb
    """
    normalizer = mcolors.Normalize(vmin=-2, vmax=2)
    colormap = plt.cm.RdYlGn

    def get(self, request: Request):
        word_rating_qs = models.WordRating.objects.all()
        word_color_dict = {}
        for word_rating_obj in word_rating_qs:
            rating = word_rating_obj.rating
            color_css = self.rating_to_csscolor(rating)
            word = word_rating_obj.word
            word_color_dict[word] = color_css
        return Response(data=word_color_dict)


    def rating_to_csscolor(self, rating):
        rating_norm = self.normalizer(rating)
        # Get only 3 first, we don't need alpha channel
        color_float = self.colormap(rating_norm)[:3]
        color_255 = tuple(int(component * 255) for component in color_float)
        # Convert the tuple to a hexadecimal color code using f-string
        color_css = f'#{color_255[0]:02x}{color_255[1]:02x}{color_255[2]:02x}'
        return color_css


class AlbumApiView(ListAPIView):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()


class SentimentApiView(ListAPIView):
    serializer_class = serializers.SongSentimentSerializer
    queryset = models.Song.objects.all()
    filterset_class = filters.FilterSongs


class SongSearchApiView(APIView):
    def post(self, request: HttpRequest):
        query = request.data.get('query')
        if query is None:
            errors = [
                {
                'type': "post_parameter_error",
                "detail": "query can't be empty",
                'instance': request.get_full_path()
                }
            ]
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        app_config = apps.get_app_config('kish_app')

        query_vector = app_config.vectorizer.transform([query])
        similarity_matrix = cosine_similarity(query_vector, app_config.corpus)
        similarity_array = np.ravel(similarity_matrix)
        best_indexes = np.argsort(similarity_array)[::-1]
        top5_index = best_indexes[:5]
        top5_similarities = similarity_array[top5_index]
        top5_df = app_config.df_songs_without_duplicates.iloc[top5_index]
        top5_titles = top5_df['title'].to_list()
        top5_lyrics = top5_df['lyrics'].to_list()

        # split to lines
        top5_lyrics = [lyrics.split('\n') for lyrics in top5_lyrics]

        data = []
        for title, lyrics_list, similarity in zip(top5_titles, top5_lyrics, top5_similarities):
            data.append({
                'title': title,
                'lyrics': lyrics_list,
                'similarity': similarity
            })
        return Response(data=data)
