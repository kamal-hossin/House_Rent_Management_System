from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class Advertisement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('rented', 'Rented'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='advertisements')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements')
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    address = models.TextField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    area_sqft = models.PositiveIntegerField()
    is_furnished = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    images = models.JSONField(default=list, blank=True)  # Store image URLs
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def mark_as_rented(self):
        self.status = 'rented'
        self.is_available = False
        self.save()
    
    def approve(self):
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.save()
    
    def reject(self):
        self.status = 'rejected'
        self.save()