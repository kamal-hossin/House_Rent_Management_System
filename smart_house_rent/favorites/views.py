from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Favorite
from .serializers import FavoriteSerializer
from advertisements.models import Advertisement

class FavoriteListView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('advertisement')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_favorites_view(request):
    """Get all favorites for the current user"""
    favorites = Favorite.objects.filter(user=request.user).select_related('advertisement')
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_favorite_view(request):
    """Add an advertisement to favorites"""
    advertisement_id = request.data.get('advertisement_id')
    if not advertisement_id:
        return Response({'error': 'advertisement_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        advertisement = Advertisement.objects.get(id=advertisement_id, status='approved', is_available=True)
    except Advertisement.DoesNotExist:
        return Response({'error': 'Advertisement not found or not available'}, status=status.HTTP_404_NOT_FOUND)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        advertisement=advertisement
    )
    
    if not created:
        return Response({'message': 'Already favorited'}, status=status.HTTP_200_OK)
    
    serializer = FavoriteSerializer(favorite)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_favorite_view(request, advertisement_id):
    """Remove an advertisement from favorites"""
    try:
        favorite = Favorite.objects.get(user=request.user, advertisement_id=advertisement_id)
        favorite.delete()
        return Response({'message': 'Removed from favorites'}, status=status.HTTP_200_OK)
    except Favorite.DoesNotExist:
        return Response({'error': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def is_favorite_view(request, advertisement_id):
    """Check if an advertisement is favorited by the current user"""
    is_favorited = Favorite.objects.filter(
        user=request.user,
        advertisement_id=advertisement_id
    ).exists()
    return Response({'is_favorited': is_favorited})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def favorites_count_view(request):
    """Get count of favorites for the current user"""
    count = Favorite.objects.filter(user=request.user).count()
    return Response({'favorites_count': count})