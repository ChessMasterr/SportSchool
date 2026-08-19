from pathlib import Path

from django import forms
from django.contrib import admin, messages

from .models import (
    CompetitionEvent,
    Document,
    GalleryAlbum,
    GalleryImage,
    News,
    ParentInfo,
    SiteSettings,
)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={'accept': 'image/*'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(item, initial) for item in data]
        return [single_file_clean(data, initial)]


class GalleryAlbumAdminForm(forms.ModelForm):
    bulk_images = MultipleFileField(
        label='Загрузить сразу несколько фото',
        required=False,
        help_text='Зажмите Ctrl (или Cmd на Mac) и выберите сразу много файлов. Можно также выделить пачку мышью.',
    )

    class Meta:
        model = GalleryAlbum
        fields = '__all__'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основное', {
            'fields': ('site_title', 'hero_title', 'hero_subtitle', 'hero_image'),
        }),
        ('Контакты и соцсети', {
            'fields': ('email', 'vk_url', 'telegram_url'),
        }),
        ('Файлы', {
            'fields': ('price_list_file',),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_type', 'school', 'is_published', 'order')
    list_filter = ('doc_type', 'school', 'is_published')
    search_fields = ('title',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'


class GalleryImageInline(admin.StackedInline):
    model = GalleryImage
    extra = 0
    fields = ('title', 'image', 'video_url', 'order', 'is_published')
    verbose_name = 'фото или видео'
    verbose_name_plural = 'Уже загруженные фото и видео'


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    form = GalleryAlbumAdminForm
    list_display = ('title', 'category', 'event_date', 'photos_count', 'school', 'is_published', 'order')
    list_filter = ('category', 'school', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryImageInline]
    fieldsets = (
        ('Мероприятие', {
            'fields': ('title', 'slug', 'category', 'event_date', 'school'),
            'description': (
                'Откройте мероприятие и загрузите сразу пачку фото в поле ниже. '
                'Уже добавленные снимки можно править или удалять в конце страницы.'
            ),
        }),
        ('Описание и обложка', {
            'fields': ('description', 'cover', 'order', 'is_published'),
        }),
        ('Массовая загрузка фото', {
            'fields': ('bulk_images',),
        }),
    )

    def photos_count(self, obj):
        return obj.items.count()
    photos_count.short_description = 'Фото / видео'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        files = form.cleaned_data.get('bulk_images') or []
        album = form.instance
        start_order = album.items.count()
        created = 0
        for index, uploaded in enumerate(files):
            title = Path(getattr(uploaded, 'name', '')).stem
            GalleryImage.objects.create(
                album=album,
                image=uploaded,
                title=title,
                order=start_order + index,
                is_published=True,
            )
            created += 1
        if created:
            messages.success(request, f'Добавлено фото: {created}')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'category', 'school', 'is_published', 'order', 'created_at')
    list_filter = ('category', 'album', 'school', 'is_published')
    search_fields = ('title', 'album__title')
    autocomplete_fields = ('album',)
    fields = ('album', 'title', 'image', 'video_url', 'order', 'is_published')


@admin.register(ParentInfo)
class ParentInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_filter = ('section',)


@admin.register(CompetitionEvent)
class CompetitionEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'school', 'is_published')
    list_filter = ('school', 'is_published')
    date_hierarchy = 'event_date'
