from django.contrib import admin
from .models import Brand, CarModel, Car, CarImage, Favorite, Message


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name']
    list_filter = ['brand']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'seller', 'price', 'city', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'brand', 'condition']
    search_fields = ['brand__name', 'model__name']
    inlines = [CarImageInline]
    list_editable = ['is_active', 'is_featured']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'car', 'is_read', 'created_at']