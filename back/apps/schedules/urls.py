from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FacilityWorkingScheduleViewSet,
    PoolSessionViewSet,
    ScheduleEntryViewSet,
    SchedulePeriodViewSet,
)

router = DefaultRouter()
router.register('schedule-periods', SchedulePeriodViewSet, basename='schedule-period')
router.register('schedule', ScheduleEntryViewSet, basename='schedule-entry')
router.register('pool-sessions', PoolSessionViewSet, basename='pool-session')
router.register('working-schedules', FacilityWorkingScheduleViewSet, basename='working-schedule')

urlpatterns = [
    path('', include(router.urls)),
]
