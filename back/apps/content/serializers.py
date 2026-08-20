from rest_framework import serializers

from .models import (
    CompetitionEvent,
    Document,
    GalleryAlbum,
    GalleryImage,
    News,
    ParentInfo,
    SiteSettings,
)


class SiteSettingsSerializer(serializers.ModelSerializer):
    hero_image_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = (
            'site_title', 'hero_title', 'hero_subtitle', 'hero_image_url',
            'email', 'vk_url', 'telegram_url',
        )

    def get_hero_image_url(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None


class DocumentSerializer(serializers.ModelSerializer):
    school_slug = serializers.CharField(
        source='school.slug', read_only=True, default=None
    )
    school_name = serializers.CharField(
        source='school.name', read_only=True, default=None
    )
    doc_type_display = serializers.CharField(source='get_doc_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = (
            'id',
            'title',
            'doc_type',
            'doc_type_display',
            'school_slug',
            'school_name',
            'file_url',
            'content',
            'order',
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
    album_slug = serializers.CharField(source='album.slug', read_only=True, default=None)
    album_title = serializers.CharField(source='album.title', read_only=True, default=None)

    class Meta:
        model = GalleryImage
        fields = (
            'id', 'title', 'image_url', 'video_url', 'category', 'category_display',
            'album', 'album_slug', 'album_title', 'school', 'order', 'created_at',
        )

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class GalleryAlbumListSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    cover_url = serializers.SerializerMethodField()
    items_count = serializers.IntegerField(read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True, default=None)

    class Meta:
        model = GalleryAlbum
        fields = (
            'id', 'title', 'slug', 'category', 'category_display',
            'description', 'event_date', 'cover_url', 'items_count',
            'school', 'school_name', 'order',
        )

    def get_cover_url(self, obj):
        request = self.context.get('request')

        def abs_url(file_field):
            if not file_field:
                return None
            if request:
                return request.build_absolute_uri(file_field.url)
            return file_field.url

        if obj.cover:
            return abs_url(obj.cover)
        first = next(
            (item for item in obj.items.all() if item.is_published and item.image),
            None,
        )
        if first:
            return abs_url(first.image)
        return None


class GalleryAlbumDetailSerializer(GalleryAlbumListSerializer):
    items = serializers.SerializerMethodField()

    class Meta(GalleryAlbumListSerializer.Meta):
        fields = GalleryAlbumListSerializer.Meta.fields + ('items',)

    def get_items(self, obj):
        published = [item for item in obj.items.all() if item.is_published]
        return GalleryImageSerializer(published, many=True, context=self.context).data


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
