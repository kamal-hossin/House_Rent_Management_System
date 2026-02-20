from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from advertisements.models import Advertisement

User = get_user_model()

class RentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='rent_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_requests')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['advertisement', 'requester']  # One request per user per advertisement
    
    def __str__(self):
        return f"{self.requester.username} - {self.advertisement.title}"
    
    def accept(self):
        # Mark the advertisement as rented
        self.advertisement.mark_as_rented()
        
        # Accept this request
        self.status = 'accepted'
        self.save()
        
        # Reject all other pending requests for this advertisement
        RentRequest.objects.filter(
            advertisement=self.advertisement,
            status='pending'
        ).exclude(id=self.id).update(status='rejected')
    
    def reject(self):
        self.status = 'rejected'
        self.save()