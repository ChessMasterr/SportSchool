from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.schools.models import Coach, Facility, SportDirection
from apps.schools.serializers import CoachSerializer, FacilitySerializer, SportDirectionSerializer

from .models import (
    CompetitionEvent,
    Document,
    GalleryImage,
    News,
    ParentInfo,
    SiteSettings,
)
from .serializers import (
    CompetitionEventSerializer,
    DocumentSerializer,
    GalleryImageSerializer,
    NewsSerializer,
    ParentInfoSerializer,
    SiteSettingsSerializer,
)


@api_view(['GET'])
def search_view(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return Response({'query': q, 'results': []})

    news = News.objects.filter(
        is_published=True,
        title__icontains=q,
    )[:10]
    sports = SportDirection.objects.filter(
        is_active=True,
        name__icontains=q,
    )[:10]
    coaches = Coach.objects.filter(
        is_active=True,
        full_name__icontains=q,
    )[:10]
    facilities = Facility.objects.filter(
        is_active=True,
    ).filter(
        Q(name__icontains=q) | Q(address__icontains=q)
    )[:10]

    return Response({
        'query': q,
        'results': {
            'news': NewsSerializer(news, many=True, context={'request': request}).data,
            'sport_directions': SportDirectionSerializer(
                sports, many=True, context={'request': request}
            ).data,
            'coaches': CoachSerializer(
                coaches, many=True, context={'request': request}
            ).data,
            'facilities': FacilitySerializer(
                facilities, many=True, context={'request': request}
            ).data,
        },
    })


@api_view(['GET'])
def site_settings_view(request):
    settings = SiteSettings.load()
    serializer = SiteSettingsSerializer(settings, context={'request': request})
    return Response(serializer.data)


class DocumentFilter(filters.FilterSet):
    doc_type = filters.CharFilter()

    class Meta:
        model = Document
        fields = ['doc_type']


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.filter(is_published=True)
    serializer_class = DocumentSerializer
    filterset_class = DocumentFilter


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    lookup_field = 'slug'


class GalleryFilter(filters.FilterSet):
    category = filters.CharFilter()
    school = filters.NumberFilter(field_name='school_id')

    class Meta:
        model = GalleryImage
        fields = ['category', 'school']


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GalleryImage.objects.filter(is_published=True).select_related('school')
    serializer_class = GalleryImageSerializer
    filterset_class = GalleryFilter


class ParentInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParentInfo.objects.all()
    serializer_class = ParentInfoSerializer


class CompetitionEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompetitionEvent.objects.filter(is_published=True).select_related('school')
    serializer_class = CompetitionEventSerializer
