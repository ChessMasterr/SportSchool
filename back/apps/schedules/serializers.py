from rest_framework import serializers

from .models import FacilityWorkingSchedule, PoolSession, ScheduleEntry, SchedulePeriod


class ScheduleEntrySerializer(serializers.ModelSerializer):
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    sport_name = serializers.CharField(
        source='sport_direction.name', read_only=True, default=''
    )
    coach_name = serializers.CharField(source='coach.full_name', read_only=True, default='')

    class Meta:
        model = ScheduleEntry
        fields = (
            'id', 'period', 'school', 'facility', 'facility_name',
            'sport_direction', 'sport_name', 'coach', 'coach_name',
            'weekday', 'weekday_display', 'time_start', 'time_end',
            'age_group', 'group_name', 'note',
        )


class PoolSessionSerializer(serializers.ModelSerializer):
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)

    class Meta:
        model = PoolSession
        fields = (
            'id', 'period', 'facility', 'facility_name',
            'weekday', 'weekday_display', 'time_start', 'time_end',
            'session_type', 'note',
        )


class SchedulePeriodSerializer(serializers.ModelSerializer):
    entries = ScheduleEntrySerializer(many=True, read_only=True)
    pool_sessions = PoolSessionSerializer(many=True, read_only=True)

    class Meta:
        model = SchedulePeriod
        fields = (
            'id', 'title', 'school', 'facility',
            'date_from', 'date_to', 'is_current', 'note',
            'entries', 'pool_sessions',
        )


class SchedulePeriodListSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True, default='')
    facility_name = serializers.CharField(source='facility.name', read_only=True, default='')

    class Meta:
        model = SchedulePeriod
        fields = (
            'id', 'title', 'school', 'school_name',
            'facility', 'facility_name',
            'date_from', 'date_to', 'is_current', 'note',
        )


class FacilityWorkingScheduleSerializer(serializers.ModelSerializer):
    weekday_display = serializers.SerializerMethodField()
    schedule_type_display = serializers.CharField(
        source='get_schedule_type_display', read_only=True
    )
    facility_name = serializers.CharField(source='facility.name', read_only=True)

    class Meta:
        model = FacilityWorkingSchedule
        fields = (
            'id', 'facility', 'facility_name', 'schedule_type',
            'schedule_type_display', 'weekday', 'weekday_display',
            'time_start', 'time_end', 'note',
        )

    def get_weekday_display(self, obj):
        if obj.weekday is None:
            return 'Ежедневно'
        return obj.get_weekday_display()
