from django.contrib import admin
from .models import RentRequest

@admin.register(RentRequest)
class RentRequestAdmin(admin.ModelAdmin):
    list_display = ['advertisement', 'requester', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['advertisement__title', 'requester__username', 'message']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['advertisement', 'requester']
    
    actions = ['accept_requests', 'reject_requests']
    
    def accept_requests(self, request, queryset):
        updated = 0
        for rent_request in queryset:
            if rent_request.status == 'pending':
                rent_request.accept()
                updated += 1
        self.message_user(request, f'{updated} rent requests were accepted.')
    accept_requests.short_description = 'Accept selected rent requests'
    
    def reject_requests(self, request, queryset):
        updated = 0
        for rent_request in queryset:
            if rent_request.status == 'pending':
                rent_request.reject()
                updated += 1
        self.message_user(request, f'{updated} rent requests were rejected.')
    reject_requests.short_description = 'Reject selected rent requests'