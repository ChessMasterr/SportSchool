from rest_framework import serializers

from .models import Coach, Facility, PriceItem, School, SportDirection


class SchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name', 'slug', 'short_description', 'opened_date', 'order')


class SchoolDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            'id', 'name', 'slug', 'short_description', 'full_description',
            'opened_date', 'order',
        )


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
    school_name = serializers.CharField(source='school.name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = SportDirection
        fields = (
            'id', 'school', 'school_name', 'facility', 'facility_name',
            'name', 'slug', 'description', 'age_from', 'age_to',
            'level', 'level_display', 'requirements', 'photo_url', 'order',
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
    class Meta:
        model = PriceItem
        fields = ('id', 'school', 'facility', 'name', 'price', 'valid_from', 'order')
