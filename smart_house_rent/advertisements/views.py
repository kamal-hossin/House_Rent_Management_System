from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters import rest_framework as filters
from django.db.models import Avg, Count
from .models import Category, Advertisement
from .serializers import CategorySerializer, AdvertisementSerializer, AdvertisementListSerializer
from users.models import User

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AdvertisementFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category_id')
    min_rent = filters.NumberFilter(field_name='rent_amount', lookup_expr='gte')
    max_rent = filters.NumberFilter(field_name='rent_amount', lookup_expr='lte')
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')
    bedrooms = filters.NumberFilter()
    bathrooms = filters.NumberFilter()
    is_furnished = filters.BooleanFilter()
    
    class Meta:
        model = Advertisement
        fields = ['category', 'min_rent', 'max_rent', 'location', 'bedrooms', 'bathrooms', 'is_furnished']

class AdvertisementListView(generics.ListCreateAPIView):
    serializer_class = AdvertisementListSerializer
    filterset_class = AdvertisementFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Only show approved and available advertisements for listing
        return Advertisement.objects.filter(status='approved', is_available=True).annotate(
            review_count=Count('reviews'),
            average_rating=Avg('reviews__rating')
        )
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AdvertisementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Advertisement.objects.all()
        return Advertisement.objects.filter(owner=user)
    
    def perform_update(self, serializer):
        # Only allow updates if not rented
        instance = self.get_object()
        if instance.status == 'rented':
            raise serializers.ValidationError("Cannot update a rented advertisement")
        serializer.save()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_advertisements_view(request):
    user = request.user
    advertisements = Advertisement.objects.filter(owner=user).annotate(
        review_count=Count('reviews'),
        average_rating=Avg('reviews__rating')
    )
    serializer = AdvertisementListSerializer(advertisements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_advertisements_view(request):
    user = request.user
    if not user.is_admin():
        return Response({'error': 'Only admins can view pending advertisements'}, status=status.HTTP_403_FORBIDDEN)
    
    advertisements = Advertisement.objects.filter(status='pending').annotate(
        review_count=Count('reviews'),
        average_rating=Avg('reviews__rating')
    )
    serializer = AdvertisementListSerializer(advertisements, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def approve_advertisement_view(request, pk):
    user = request.user
    if not user.is_admin():
        return Response({'error': 'Only admins can approve advertisements'}, status=status.HTTP_403_FORBIDDEN)
    
    advertisement = generics.get_object_or_404(Advertisement, pk=pk)
    advertisement.approve()
    
    serializer = AdvertisementSerializer(advertisement)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def reject_advertisement_view(request, pk):
    user = request.user
    if not user.is_admin():
        return Response({'error': 'Only admins can reject advertisements'}, status=status.HTTP_403_FORBIDDEN)
    
    advertisement = generics.get_object_or_404(Advertisement, pk=pk)
    advertisement.reject()
    
    serializer = AdvertisementSerializer(advertisement)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def rented_advertisements_view(request):
    user = request.user
    advertisements = Advertisement.objects.filter(status='rented', owner=user).annotate(
        review_count=Count('reviews'),
        average_rating=Avg('reviews__rating')
    )
    serializer = AdvertisementListSerializer(advertisements, many=True)
    return Response(serializer.data)