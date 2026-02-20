from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import RentRequest
from .serializers import RentRequestSerializer, RentRequestActionSerializer
from advertisements.models import Advertisement
from users.models import User

class RentRequestListView(generics.ListCreateAPIView):
    serializer_class = RentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Show requests for advertisements owned by the user, or requests made by the user
        return RentRequest.objects.filter(
            models.Q(advertisement__owner=user) | models.Q(requester=user)
        ).select_related('advertisement', 'requester')
    
    def perform_create(self, serializer):
        advertisement = serializer.validated_data['advertisement']
        
        # Check if user already has a pending request for this advertisement
        if RentRequest.objects.filter(
            advertisement=advertisement,
            requester=self.request.user,
            status='pending'
        ).exists():
            raise serializers.ValidationError("You already have a pending request for this advertisement")
        
        # Check if advertisement is already rented
        if advertisement.status == 'rented':
            raise serializers.ValidationError("This advertisement is already rented")
        
        serializer.save(requester=self.request.user)

class RentRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RentRequest.objects.all()
    serializer_class = RentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Users can only see their own requests or requests for their advertisements
        return RentRequest.objects.filter(
            models.Q(advertisement__owner=user) | models.Q(requester=user)
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_rent_requests_view(request):
    """Get all rent requests made by the current user"""
    rent_requests = RentRequest.objects.filter(requester=request.user).select_related('advertisement', 'requester')
    serializer = RentRequestSerializer(rent_requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_advertisement_requests_view(request):
    """Get all rent requests for advertisements owned by the current user"""
    rent_requests = RentRequest.objects.filter(advertisement__owner=request.user).select_related('advertisement', 'requester')
    serializer = RentRequestSerializer(rent_requests, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def rent_request_action_view(request, pk, action):
    """Accept or reject a rent request"""
    rent_request = generics.get_object_or_404(RentRequest, pk=pk)
    
    # Only the advertisement owner can accept/reject requests
    if rent_request.advertisement.owner != request.user:
        return Response({'error': 'You can only manage requests for your own advertisements'}, status=status.HTTP_403_FORBIDDEN)
    
    if action == 'accept':
        rent_request.accept()
    elif action == 'reject':
        rent_request.reject()
    else:
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = RentRequestSerializer(rent_request)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_requests_count_view(request):
    """Get count of pending rent requests for the current user's advertisements"""
    count = RentRequest.objects.filter(
        advertisement__owner=request.user,
        status='pending'
    ).count()
    return Response({'pending_requests_count': count})