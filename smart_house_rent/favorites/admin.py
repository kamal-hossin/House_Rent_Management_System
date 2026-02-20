from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'advertisement', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'advertisement__title']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'advertisement']