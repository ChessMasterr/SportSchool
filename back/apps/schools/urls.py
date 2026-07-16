from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CoachViewSet,
    FacilityViewSet,
    PriceItemViewSet,
    SchoolViewSet,
    SportDirectionViewSet,
)

router = DefaultRouter()
router.register('schools', SchoolViewSet, basename='school')
router.register('facilities', FacilityViewSet, basename='facility')
router.register('sport-directions', SportDirectionViewSet, basename='sport-direction')
router.register('coaches', CoachViewSet, basename='coach')
router.register('prices', PriceItemViewSet, basename='price')

urlpatterns = [
    path('', include(router.urls)),
]
