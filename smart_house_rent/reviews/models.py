from django.db import models
from django.contrib.auth import get_user_model
from advertisements.models import Advertisement
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Review(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=models.DateTimeField(auto_now_add=True))
    
    class Meta:
        unique_together = ['advertisement', 'reviewer']  # One review per user per advertisement
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reviewer.username} - {self.advertisement.title} - {self.rating}/5"
    
    @property
    def advertisement_title(self):
        return self.advertisement.title