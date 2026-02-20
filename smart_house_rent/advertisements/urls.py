from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('advertisements/', views.AdvertisementListView.as_view(), name='advertisement-list'),
    path('advertisements/<int:pk>/', views.AdvertisementDetailView.as_view(), name='advertisement-detail'),
    path('my-advertisements/', views.my_advertisements_view, name='my-advertisements'),
    path('pending-advertisements/', views.pending_advertisements_view, name='pending-advertisements'),
    path('advertisements/<int:pk>/approve/', views.approve_advertisement_view, name='approve-advertisement'),
    path('advertisements/<int:pk>/reject/', views.reject_advertisement_view, name='reject-advertisement'),
    path('rented-advertisements/', views.rented_advertisements_view, name='rented-advertisements'),
]