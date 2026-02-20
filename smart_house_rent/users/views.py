from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_verified:
                auth_login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Login successful',
                    'token': token.key,
                    'user': UserProfileSerializer(user).data
                })
            else:
                return Response({
                    'error': 'Email not verified. Please check your email for verification link.'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    auth_logout(request)
    return Response({'message': 'Logged out successfully'})

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    user = request.user
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_advertisements_view(request):
    user = request.user
    advertisements = user.advertisements.all()
    from advertisements.serializers import AdvertisementListSerializer
    serializer = AdvertisementListSerializer(advertisements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_rent_requests_view(request):
    user = request.user
    rent_requests = user.rent_requests.all()
    from rent_requests.serializers import RentRequestSerializer
    serializer = RentRequestSerializer(rent_requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_favorites_view(request):
    user = request.user
    favorites = user.favorites.all()
    from favorites.serializers import FavoriteSerializer
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_reviews_view(request):
    user = request.user
    reviews = user.reviews.all()
    from reviews.serializers import ReviewSerializer
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_email_view(request, token):
    user = get_object_or_404(User, verification_token=token)
    user.is_verified = True
    user.verification_token = None
    user.save()
    return Response({'message': 'Email verified successfully'})