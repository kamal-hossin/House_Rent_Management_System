from django.contrib import admin
from .models import Category, Advertisement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'owner', 'category', 'rent_amount', 'status', 
        'is_available', 'is_furnished', 'created_at', 'approved_at'
    ]
    list_filter = [
        'status', 'is_available', 'is_furnished', 'category', 
        'bedrooms', 'bathrooms', 'created_at', 'approved_at'
    ]
    search_fields = ['title', 'description', 'location', 'address']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']
    raw_id_fields = ['owner']
    
    actions = ['approve_advertisements', 'reject_advertisements', 'mark_as_rented']
    
    def approve_advertisements(self, request, queryset):
        updated = 0
        for advertisement in queryset:
            if advertisement.status != 'approved':
                advertisement.approve()
                updated += 1
        self.message_user(request, f'{updated} advertisements were approved.')
    approve_advertisements.short_description = 'Approve selected advertisements'
    
    def reject_advertisements(self, request, queryset):
        updated = 0
        for advertisement in queryset:
            if advertisement.status != 'rejected':
                advertisement.reject()
                updated += 1
        self.message_user(request, f'{updated} advertisements were rejected.')
    reject_advertisements.short_description = 'Reject selected advertisements'
    
    def mark_as_rented(self, request, queryset):
        updated = 0
        for advertisement in queryset:
            if advertisement.status != 'rented':
                advertisement.mark_as_rented()
                updated += 1
        self.message_user(request, f'{updated} advertisements were marked as rented.')
    mark_as_rented.short_description = 'Mark selected advertisements as rented'