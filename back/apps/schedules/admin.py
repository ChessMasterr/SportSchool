from django.contrib import admin

from .models import (
    FacilityWorkingSchedule,
    PoolSession,
    ScheduleEntry,
    SchedulePeriod,
)


class ScheduleEntryInline(admin.TabularInline):
    model = ScheduleEntry
    extra = 1
    fields = (
        'weekday', 'time_start', 'time_end', 'sport_direction',
        'coach', 'age_group', 'group_name', 'facility',
    )
    autocomplete_fields = ['sport_direction', 'coach', 'facility']


class PoolSessionInline(admin.TabularInline):
    model = PoolSession
    extra = 1
    fields = ('weekday', 'time_start', 'time_end', 'session_type', 'facility', 'note')


@admin.register(SchedulePeriod)
class SchedulePeriodAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'facility', 'date_from', 'date_to', 'is_current')
    list_filter = ('is_current', 'school', 'facility')
    search_fields = ('title',)
    inlines = [ScheduleEntryInline, PoolSessionInline]


@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = (
        'period', 'facility', 'sport_direction', 'coach',
        'weekday', 'time_start', 'time_end', 'age_group',
    )
    list_filter = ('period', 'school', 'facility', 'weekday', 'sport_direction')
    search_fields = ('group_name', 'age_group')
    autocomplete_fields = ['period', 'school', 'facility', 'sport_direction', 'coach']


@admin.register(PoolSession)
class PoolSessionAdmin(admin.ModelAdmin):
    list_display = ('period', 'facility', 'weekday', 'time_start', 'time_end', 'session_type')
    list_filter = ('period', 'facility', 'weekday')
    autocomplete_fields = ['period', 'facility']


@admin.register(FacilityWorkingSchedule)
class FacilityWorkingScheduleAdmin(admin.ModelAdmin):
    list_display = ('facility', 'schedule_type', 'weekday', 'time_start', 'time_end')
    list_filter = ('facility', 'schedule_type')
    autocomplete_fields = ['facility']
