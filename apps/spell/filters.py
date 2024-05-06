import django_filters
from apps.spell.apps import Spell


class SpellFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method='filter_by_search_query')

    def filter_by_search_query(self, queryset, name, value):
        return queryset.filter(tradition__iexact=value)

    class Meta:
        model = Spell
        fields = ['search_query']
