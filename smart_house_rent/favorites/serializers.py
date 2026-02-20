from rest_framework import serializers
from .models import Favorite
from advertisements.serializers import AdvertisementListSerializer
from advertisements.models import Advertisement

class FavoriteSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementListSerializer(read_only=True)
    advertisement_id = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.none(),  # Will be set in __init__
        source='advertisement',
        write_only=True
    )
    
    class Meta:
        model = Favorite
        fields = ['id', 'advertisement', 'advertisement_id', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show approved and available advertisements
        self.fields['advertisement_id'].queryset = self.get_advertisement_queryset()
    
    def get_advertisement_queryset(self):
        from advertisements.models import Advertisement
        return Advertisement.objects.filter(status='approved', is_available=True)
    
    def validate_advertisement_id(self, value):
        # Check if advertisement is approved and available
        if value.status != 'approved' or not value.is_available:
            raise serializers.ValidationError("Cannot favorite this advertisement")
        return value
    
    def validate(self, attrs):
        advertisement = attrs.get('advertisement')
        user = self.context['request'].user
        
        # Check if already favorited
        if Favorite.objects.filter(user=user, advertisement=advertisement).exists():
            raise serializers.ValidationError("You have already favorited this advertisement")
        
        return attrs