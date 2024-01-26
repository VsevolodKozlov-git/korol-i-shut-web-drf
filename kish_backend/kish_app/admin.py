from django.contrib import admin
from kish_app import models

# Register your models here.
models_to_reg = [
    models.Song,
    models.Album,
    models.WordRating
]
for model in models_to_reg:
    admin.site.register(model)
