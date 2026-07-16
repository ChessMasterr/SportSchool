from django.contrib import admin

from .models import Coach, Facility, PriceItem, School, SportDirection


class FacilityInline(admin.TabularInline):
    model = Facility
    extra = 0
    fields = ('name', 'facility_type', 'address', 'phone', 'working_hours', 'is_active', 'order')


class SportDirectionInline(admin.TabularInline):
    model = SportDirection
    extra = 0
    fields = ('name', 'age_from', 'age_to', 'is_active', 'order')


class PriceItemInline(admin.TabularInline):
    model = PriceItem
    extra = 0
    fields = ('name', 'price', 'valid_from', 'order')


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'opened_date', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FacilityInline, SportDirectionInline, PriceItemInline]


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'facility_type', 'phone', 'working_hours', 'is_active')
    list_filter = ('school', 'facility_type', 'has_hall_rental', 'is_active')
    search_fields = ('name', 'address')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SportDirection)
class SportDirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'facility', 'age_from', 'age_to', 'is_active')
    list_filter = ('school', 'facility', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'school', 'facility', 'is_active', 'order')
    list_filter = ('school', 'facility', 'is_active')
    search_fields = ('full_name',)
    filter_horizontal = ('sport_directions',)


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'facility', 'price', 'valid_from', 'order')
    list_filter = ('school', 'facility')
    search_fields = ('name',)
