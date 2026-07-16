from rest_framework import serializers

from .models import (
    CompetitionEvent,
    Document,
    GalleryImage,
    News,
    ParentInfo,
    SiteSettings,
)


class SiteSettingsSerializer(serializers.ModelSerializer):
    hero_image_url = serializers.SerializerMethodField()
    price_list_file_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = (
            'site_title', 'hero_title', 'hero_subtitle', 'hero_image_url',
            'email', 'vk_url', 'telegram_url', 'price_list_file_url',
        )

    def get_hero_image_url(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None

    def get_price_list_file_url(self, obj):
        if obj.price_list_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.price_list_file.url)
            return obj.price_list_file.url
        return None


class DocumentSerializer(serializers.ModelSerializer):
    doc_type_display = serializers.CharField(source='get_doc_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = (
            'id', 'title', 'doc_type', 'doc_type_display',
            'file_url', 'content', 'order',
        )

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class NewsSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            'id', 'title', 'slug', 'body', 'category', 'category_display',
            'image_url', 'video_url', 'published_at',
        )

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class GalleryImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = GalleryImage
        fields = (
            'id', 'title', 'image_url', 'category', 'category_display',
            'school', 'order', 'created_at',
        )

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ParentInfoSerializer(serializers.ModelSerializer):
    section_display = serializers.CharField(source='get_section_display', read_only=True)

    class Meta:
        model = ParentInfo
        fields = ('id', 'section', 'section_display', 'title', 'content', 'order')


class CompetitionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionEvent
        fields = (
            'id', 'title', 'description', 'event_date',
            'location', 'school',
        )
