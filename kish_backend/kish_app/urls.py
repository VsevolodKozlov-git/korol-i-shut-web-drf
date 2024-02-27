from kish_app import views
from django.urls import path, include

urlpatterns = [
    path('word_cloud/all', views.WordCloudAllApiView.as_view(), name='word_cloud_all'),
    path('word_cloud/word_frequency', views.WordFreqApiView.as_view(), name='word_cloud__word_frequency'),
    path('word_cloud/word_color', views.WordColorApiView.as_view(), name='word_cloud__word_color'),
    path('album/list', views.AlbumApiView.as_view(), name='album_list'),
    path('vizualization/sentiment', views.SentimentApiView.as_view(), name='vizualization_sentiment'),
    path('song/search', views.SongSearchApiView.as_view())
]