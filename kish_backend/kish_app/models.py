from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

word_max_length = 50
title_max_length = 200


class Song(models.Model):
    title = models.CharField(max_length=title_max_length)
    lyrics = models.TextField()
    album = models.ForeignKey('Album',
                              related_name='songs',
                              on_delete=models.RESTRICT)
    tokens = ArrayField(models.CharField(max_length=word_max_length))
    adjectives = ArrayField(models.CharField(max_length=word_max_length))
    verbs = ArrayField(models.CharField(max_length=word_max_length))
    nouns = ArrayField(models.CharField(max_length=word_max_length))
    negative = models.FloatField(null=False)
    positive = models.FloatField(null=False)
    neutral = models.FloatField(null=False)



    def __str__(self):
        return f'"{self.title}" {self.album}'


class Album(models.Model):
    title = models.CharField(max_length=title_max_length)
    year = models.IntegerField()

    def __str__(self):
        return f'{self.title}'


class WordRating(models.Model):
    word = models.CharField(max_length=word_max_length, db_index=True)
    rating = models.FloatField()

    def __str__(self):
        return f'{self.word} {round(self.rating, 2)}'