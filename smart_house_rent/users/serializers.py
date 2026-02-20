from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import secrets

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_type', 'is_verified', 'created_at']
        read_only_fields = ['id', 'user_type', 'is_verified', 'created_at']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        
        # Generate verification token
        user.verification_token = secrets.token_urlsafe(32)
        user.save()
        
        # Send verification email
        self.send_verification_email(user)
        
        return user
    
    def send_verification_email(self, user):
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{user.verification_token}/"
        
        subject = 'Verify your email address'
        message = f'''
        Hi {user.username},
        
        Thank you for registering! Please click the link below to verify your email address:
        
        {verification_url}
        
        If you did not create an account, please ignore this email.
        '''
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'is_verified', 'created_at']
        read_only_fields = ['id', 'user_type', 'is_verified', 'created_at']