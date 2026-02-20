from rest_framework import serializers
from .models import RentRequest
from advertisements.models import Advertisement
from users.models import User

class RentRequestSerializer(serializers.ModelSerializer):
    advertisement_title = serializers.CharField(source='advertisement.title', read_only=True)
    advertisement_owner = serializers.CharField(source='advertisement.owner.username', read_only=True)
    requester_name = serializers.CharField(source='requester.username', read_only=True)
    
    class Meta:
        model = RentRequest
        fields = [
            'id', 'advertisement', 'advertisement_title', 'advertisement_owner',
            'requester', 'requester_name', 'message', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'advertisement_owner', 'requester_name', 'status', 'created_at', 'updated_at']
    
    def validate_advertisement(self, value):
        # Check if advertisement is already rented
        if value.status == 'rented':
            raise serializers.ValidationError("This advertisement is already rented")
        
        # Check if advertisement is approved
        if value.status != 'approved':
            raise serializers.ValidationError("Only approved advertisements can receive rent requests")
        
        return value
    
    def validate(self, attrs):
        advertisement = attrs.get('advertisement')
        requester = self.context['request'].user
        
        # Check if user already has a pending request for this advertisement
        if RentRequest.objects.filter(
            advertisement=advertisement,
            requester=requester,
            status='pending'
        ).exists():
            raise serializers.ValidationError("You already have a pending request for this advertisement")
        
        # Check if user is the owner of the advertisement
        if advertisement.owner == requester:
            raise serializers.ValidationError("You cannot send a rent request for your own advertisement")
        
        return attrs

class RentRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['accept', 'reject'])