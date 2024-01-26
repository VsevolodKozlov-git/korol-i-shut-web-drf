from kish_app import views
from django.urls import path, include

urlpatterns = [
    path('word_cloud/all', views.WordCloudAllApiView.as_view(), name='word_cloud_all'),
    path('word_cloud/word_frequency', views.GetWordFreq.as_view(), name='word_clod__word_frequency')
]