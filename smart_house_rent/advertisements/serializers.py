from rest_framework import serializers
from .models import Category, Advertisement
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']

class AdvertisementSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Advertisement
        fields = [
            'id', 'title', 'description', 'category', 'category_name', 'category_id',
            'owner', 'rent_amount', 'security_deposit', 'location', 'address',
            'bedrooms', 'bathrooms', 'area_sqft', 'is_furnished', 'is_available',
            'status', 'images', 'created_at', 'updated_at', 'approved_at', 'is_owner'
        ]
        read_only_fields = ['id', 'owner', 'status', 'created_at', 'updated_at', 'approved_at']
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.owner == request.user
        return False
    
    def validate(self, attrs):
        # Only admins can approve/reject advertisements
        if 'status' in attrs and attrs['status'] in ['approved', 'rejected']:
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                if not request.user.is_admin():
                    raise serializers.ValidationError("Only admins can approve or reject advertisements")
        return attrs

class AdvertisementListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Advertisement
        fields = [
            'id', 'title', 'description', 'category_name', 'owner',
            'rent_amount', 'location', 'bedrooms', 'bathrooms', 'area_sqft',
            'is_furnished', 'status', 'images', 'created_at', 'review_count', 'average_rating'
        ]