from django.urls import path
from . import views

urlpatterns = [
    path('rent-requests/', views.RentRequestListView.as_view(), name='rent-request-list'),
    path('rent-requests/<int:pk>/', views.RentRequestDetailView.as_view(), name='rent-request-detail'),
    path('my-rent-requests/', views.my_rent_requests_view, name='my-rent-requests'),
    path('my-advertisement-requests/', views.my_advertisement_requests_view, name='my-advertisement-requests'),
    path('rent-requests/<int:pk>/<str:action>/', views.rent_request_action_view, name='rent-request-action'),
    path('pending-requests-count/', views.pending_requests_count_view, name='pending-requests-count'),
]