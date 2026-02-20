from rest_framework import serializers
from .models import Review
from advertisements.models import Advertisement
from users.models import User

class ReviewSerializer(serializers.ModelSerializer):
    advertisement_title = serializers.CharField(source='advertisement.title', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'advertisement', 'advertisement_title', 'reviewer', 'reviewer_name',
            'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'advertisement_title', 'reviewer', 'reviewer_name', 'created_at']
    
    def validate_advertisement(self, value):
        # Check if advertisement is approved
        if value.status != 'approved':
            raise serializers.ValidationError("Reviews can only be added to approved advertisements")
        return value
    
    def validate(self, attrs):
        advertisement = attrs.get('advertisement')
        reviewer = self.context['request'].user
        
        # Check if user already reviewed this advertisement
        if Review.objects.filter(advertisement=advertisement, reviewer=reviewer).exists():
            raise serializers.ValidationError("You have already reviewed this advertisement")
        
        # Check if user is the owner of the advertisement
        if advertisement.owner == reviewer:
            raise serializers.ValidationError("You cannot review your own advertisement")
        
        # Check if user has rented this advertisement (optional requirement)
        # This would require checking rent requests, but for now we'll allow any user to review
        
        return attrs