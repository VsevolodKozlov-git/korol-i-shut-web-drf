import django_filters as filters
from kish_app import models


class FilterAlbumsByYear(filters.FilterSet):
    year = filters.NumericRangeFilter(field_name='year')

    class Meta:
        model = models.Album
        fields = ['year']