from django.contrib import admin

from .models import (
    CompetitionEvent,
    Document,
    GalleryImage,
    News,
    ParentInfo,
    SiteSettings,
)


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
    list_display = ('title', 'doc_type', 'is_published', 'order')
    list_filter = ('doc_type', 'is_published')
    search_fields = ('title',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'school', 'is_published', 'order', 'created_at')
    list_filter = ('category', 'school', 'is_published')
    search_fields = ('title',)


@admin.register(ParentInfo)
class ParentInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_filter = ('section',)


@admin.register(CompetitionEvent)
class CompetitionEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'school', 'is_published')
    list_filter = ('school', 'is_published')
    date_hierarchy = 'event_date'
