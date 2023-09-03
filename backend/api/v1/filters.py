from django_filters import FilterSet
from django_filters import rest_framework as filters
from trainings.models import Training


class TrainingsFilter(FilterSet):
    """
    Filter for TrainingsViewSet.
    """
    started = filters.DateTimeFromToRangeFilter(field_name='started_at')

    class Meta:
        model = Training
        fields = ('started_at',)
