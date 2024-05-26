import django_filters as filters
from kish_app import models
from abc import ABC, abstractmethod


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class FilterSongs(filters.FilterSet):
    year = filters.RangeFilter(field_name='album__year')
    albums_titles = CharInFilter(field_name='album__title')

    class Meta:
        model = models.Song
        fields = ['album']


class CustomFilter(ABC):
    def __init__(self, request):
        self.errors = []
        self.data = None
        self.handle_request(request)

    @abstractmethod
    def handle_request(self, request):
        pass


class TagTypeFilter(CustomFilter):
    # 1value = get parameter value
    # 2value = data value associated with get parameter
    parameter_to_data = {
        'all': 'tokens',
        'adjectives': 'adjectives',
        'nouns': 'nouns',
        'verbs': 'verbs',
    }

    def handle_request(self, request):
        url = request.get_full_path()
        tag_type = request.query_params.get('tag_type')
        # error handling
        if tag_type is None:
            self.errors.append(
                {
                    'type': "get_parameter_error",
                    "detail": 'not provided tag_type in get request parameters',
                    'instance': url,
                }
            )
            return
        if tag_type not in self.parameter_to_data.keys():
            self.errors.append(
                {
                    'type': "get_parameter_error",
                    "detail": "tag type should be one of the following ['all', 'nouns', 'verbs', 'adjectives']",
                    'instance': url,
                }
            )
            return

        self.data = self.parameter_to_data[tag_type]
