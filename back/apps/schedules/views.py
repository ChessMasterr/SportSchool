from django_filters import rest_framework as filters
from rest_framework import viewsets

from .models import FacilityWorkingSchedule, PoolSession, ScheduleEntry, SchedulePeriod
from .serializers import (
    FacilityWorkingScheduleSerializer,
    PoolSessionSerializer,
    ScheduleEntrySerializer,
    SchedulePeriodListSerializer,
    SchedulePeriodSerializer,
)


class SchedulePeriodFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name='school_id')
    school_slug = filters.CharFilter(field_name='school__slug')
    facility = filters.NumberFilter(field_name='facility_id')
    is_current = filters.BooleanFilter()

    class Meta:
        model = SchedulePeriod
        fields = ['school', 'school_slug', 'facility', 'is_current']


class SchedulePeriodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchedulePeriod.objects.select_related('school', 'facility').prefetch_related(
        'entries__sport_direction',
        'entries__coach',
        'entries__facility',
        'pool_sessions__facility',
    )
    filterset_class = SchedulePeriodFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchedulePeriodSerializer
        return SchedulePeriodListSerializer


class ScheduleEntryFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name='school_id')
    school_slug = filters.CharFilter(field_name='school__slug')
    facility = filters.NumberFilter(field_name='facility_id')
    sport_direction = filters.NumberFilter(field_name='sport_direction_id')
    coach = filters.NumberFilter(field_name='coach_id')
    weekday = filters.NumberFilter()
    period = filters.NumberFilter(field_name='period_id')

    class Meta:
        model = ScheduleEntry
        fields = [
            'school', 'school_slug', 'facility',
            'sport_direction', 'coach', 'weekday', 'period',
        ]


class ScheduleEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScheduleEntry.objects.select_related(
        'period', 'school', 'facility', 'sport_direction', 'coach',
    )
    serializer_class = ScheduleEntrySerializer
    filterset_class = ScheduleEntryFilter


class PoolSessionFilter(filters.FilterSet):
    facility = filters.NumberFilter(field_name='facility_id')
    period = filters.NumberFilter(field_name='period_id')
    weekday = filters.NumberFilter()

    class Meta:
        model = PoolSession
        fields = ['facility', 'period', 'weekday']


class PoolSessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PoolSession.objects.select_related('period', 'facility')
    serializer_class = PoolSessionSerializer
    filterset_class = PoolSessionFilter


class FacilityWorkingScheduleFilter(filters.FilterSet):
    facility = filters.NumberFilter(field_name='facility_id')

    class Meta:
        model = FacilityWorkingSchedule
        fields = ['facility']


class FacilityWorkingScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FacilityWorkingSchedule.objects.select_related('facility')
    serializer_class = FacilityWorkingScheduleSerializer
    filterset_class = FacilityWorkingScheduleFilter
