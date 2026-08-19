from rest_framework import serializers

from .models import Coach, Facility, PriceItem, School, SportDirection


class SchoolListSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = (
            'id', 'name', 'slug', 'short_description',
            'opened_date', 'order', 'photo_url',
        )

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class SchoolDetailSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = (
            'id', 'name', 'slug', 'short_description', 'full_description',
            'opened_date', 'order', 'photo_url',
        )

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class FacilitySerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = (
            'id', 'school', 'school_name', 'name', 'slug', 'facility_type',
            'address', 'phone', 'phone_admin', 'working_hours', 'description',
            'has_hall_rental', 'hall_rental_note', 'latitude', 'longitude',
            'photo_url', 'order',
        )

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class SportDirectionSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True, default=None)
    school_slug = serializers.CharField(source='school.slug', read_only=True, default=None)
    facility_name = serializers.CharField(source='facility.name', read_only=True, default=None)
    facility_slug = serializers.CharField(source='facility.slug', read_only=True, default=None)
    facility_address = serializers.CharField(source='facility.address', read_only=True, default=None)
    facility_phone = serializers.CharField(source='facility.phone', read_only=True, default=None)
    facility_working_hours = serializers.CharField(
        source='facility.working_hours', read_only=True, default=None
    )
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = SportDirection
        fields = (
            'id', 'school', 'school_name', 'facility', 'facility_name',
            'facility_slug', 'facility_address', 'facility_phone',
            'facility_working_hours', 'name', 'slug', 'description',
            'age_from', 'age_to', 'level', 'level_display', 'requirements',
            'school_slug',
            'photo_url',
            'order',
        )

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class CoachSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    sport_directions_list = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = (
            'id', 'school', 'school_name', 'facility', 'facility_name',
            'full_name', 'photo_url', 'education', 'qualification',
            'sports_titles', 'experience', 'achievements',
            'sport_directions_list', 'order',
        )

    def get_sport_directions_list(self, obj):
        return list(obj.sport_directions.values_list('name', flat=True))

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class PriceItemSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True, default=None)
    school_slug = serializers.CharField(source='school.slug', read_only=True, default=None)
    facility_name = serializers.CharField(source='facility.name', read_only=True, default=None)

    class Meta:
        model = PriceItem
        fields = (
            'id', 'school', 'school_name', 'school_slug',
            'facility', 'facility_name', 'name', 'price', 'valid_from', 'order',
        )
