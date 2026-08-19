from django_filters import rest_framework as filters
from rest_framework import viewsets

from .models import Coach, Facility, PriceItem, School, SportDirection
from .serializers import (
    CoachSerializer,
    FacilitySerializer,
    PriceItemSerializer,
    SchoolDetailSerializer,
    SchoolListSerializer,
    SportDirectionSerializer,
)


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.filter(is_active=True)
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolDetailSerializer
        return SchoolListSerializer


class FacilityFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name='school_id')
    school_slug = filters.CharFilter(field_name='school__slug')
    facility_type = filters.CharFilter()

    class Meta:
        model = Facility
        fields = ['school', 'school_slug', 'facility_type', 'has_hall_rental']


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Facility.objects.filter(is_active=True).select_related('school')
    serializer_class = FacilitySerializer
    lookup_field = 'slug'
    filterset_class = FacilityFilter


class SportDirectionFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name='school_id')
    school_slug = filters.CharFilter(field_name='school__slug')
    facility = filters.NumberFilter(field_name='facility_id')

    class Meta:
        model = SportDirection
        fields = ['school', 'school_slug', 'facility']


class SportDirectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SportDirection.objects.filter(is_active=True).select_related(
        'school', 'facility'
    )
    serializer_class = SportDirectionSerializer
    lookup_field = 'slug'
    filterset_class = SportDirectionFilter


class CoachFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name='school_id')
    school_slug = filters.CharFilter(field_name='school__slug')
    facility = filters.NumberFilter(field_name='facility_id')
    sport_direction = filters.NumberFilter(field_name='sport_directions')

    class Meta:
        model = Coach
        fields = ['school', 'school_slug', 'facility', 'sport_direction']


class CoachViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coach.objects.filter(is_active=True).select_related(
        'school', 'facility'
    ).prefetch_related('sport_directions')
    serializer_class = CoachSerializer
    filterset_class = CoachFilter


class PriceItemFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name='school_id')
    school_slug = filters.CharFilter(field_name='school__slug')
    facility = filters.NumberFilter(field_name='facility_id')

    class Meta:
        model = PriceItem
        fields = ['school', 'school_slug', 'facility']


class PriceItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceItem.objects.select_related('school', 'facility')
    serializer_class = PriceItemSerializer
    filterset_class = PriceItemFilter
    pagination_class = None
