from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Review
from .serializers import ReviewSerializer
from advertisements.models import Advertisement

class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        advertisement_id = self.kwargs.get('advertisement_id')
        if advertisement_id:
            return Review.objects.filter(advertisement_id=advertisement_id).select_related('advertisement', 'reviewer')
        return Review.objects.filter(reviewer=self.request.user).select_related('advertisement', 'reviewer')
    
    def perform_create(self, serializer):
        advertisement_id = self.kwargs.get('advertisement_id')
        if advertisement_id:
            advertisement = generics.get_object_or_404(Advertisement, id=advertisement_id)
            serializer.save(reviewer=self.request.user, advertisement=advertisement)
        else:
            serializer.save(reviewer=self.request.user)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Users can only see their own reviews or reviews for advertisements they own
        return Review.objects.filter(
            models.Q(reviewer=user) | models.Q(advertisement__owner=user)
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_reviews_view(request):
    """Get all reviews made by the current user"""
    reviews = Review.objects.filter(reviewer=request.user).select_related('advertisement', 'reviewer')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def advertisement_reviews_view(request, advertisement_id):
    """Get all reviews for a specific advertisement"""
    reviews = Review.objects.filter(advertisement_id=advertisement_id).select_related('advertisement', 'reviewer')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_advertisement_reviews_view(request):
    """Get all reviews for advertisements owned by the current user"""
    reviews = Review.objects.filter(advertisement__owner=request.user).select_related('advertisement', 'reviewer')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_review_view(request, advertisement_id):
    """Create a review for an advertisement"""
    try:
        advertisement = Advertisement.objects.get(id=advertisement_id, status='approved')
    except Advertisement.DoesNotExist:
        return Response({'error': 'Advertisement not found or not approved'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if user already reviewed this advertisement
    if Review.objects.filter(advertisement=advertisement, reviewer=request.user).exists():
        return Response({'error': 'You have already reviewed this advertisement'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user is the owner of the advertisement
    if advertisement.owner == request.user:
        return Response({'error': 'You cannot review your own advertisement'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(reviewer=request.user, advertisement=advertisement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def can_review_view(request, advertisement_id):
    """Check if the user can review an advertisement"""
    try:
        advertisement = Advertisement.objects.get(id=advertisement_id, status='approved')
    except Advertisement.DoesNotExist:
        return Response({'can_review': False, 'reason': 'Advertisement not found or not approved'})
    
    # Check if user already reviewed this advertisement
    if Review.objects.filter(advertisement=advertisement, reviewer=request.user).exists():
        return Response({'can_review': False, 'reason': 'Already reviewed'})
    
    # Check if user is the owner of the advertisement
    if advertisement.owner == request.user:
        return Response({'can_review': False, 'reason': 'Cannot review own advertisement'})
    
    return Response({'can_review': True})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def advertisement_rating_view(request, advertisement_id):
    """Get average rating and review count for an advertisement"""
    try:
        advertisement = Advertisement.objects.get(id=advertisement_id, status='approved')
    except Advertisement.DoesNotExist:
        return Response({'error': 'Advertisement not found or not approved'}, status=status.HTTP_404_NOT_FOUND)
    
    reviews = Review.objects.filter(advertisement=advertisement)
    avg_rating = reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
    review_count = reviews.count()
    
    return Response({
        'advertisement_id': advertisement_id,
        'average_rating': round(avg_rating, 2),
        'review_count': review_count
    })