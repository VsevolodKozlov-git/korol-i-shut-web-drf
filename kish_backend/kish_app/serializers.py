from rest_framework import serializers
from kish_app import models


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        exclude = ['id']


class SongSentimentSerializer(serializers.ModelSerializer):
    album = AlbumSerializer()
    class Meta:
        model = models.Song
        fields = ['title', 'album', 'negative', 'positive', 'neutral']