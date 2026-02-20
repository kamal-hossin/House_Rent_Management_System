from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['advertisement', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['advertisement__title', 'reviewer__username', 'comment']
    readonly_fields = ['created_at']
    raw_id_fields = ['advertisement', 'reviewer']