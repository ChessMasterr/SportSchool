from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CompetitionEventViewSet,
    DocumentViewSet,
    GalleryAlbumViewSet,
    GalleryViewSet,
    NewsViewSet,
    ParentInfoViewSet,
    search_view,
    site_settings_view,
)

router = DefaultRouter()
router.register('documents', DocumentViewSet, basename='document')
router.register('news', NewsViewSet, basename='news')
router.register('gallery/albums', GalleryAlbumViewSet, basename='gallery-album')
router.register('gallery', GalleryViewSet, basename='gallery')
router.register('parents', ParentInfoViewSet, basename='parent-info')
router.register('competitions', CompetitionEventViewSet, basename='competition')

urlpatterns = [
    path('site-settings/', site_settings_view, name='site-settings'),
    path('search/', search_view, name='search'),
    path('', include(router.urls)),
]
