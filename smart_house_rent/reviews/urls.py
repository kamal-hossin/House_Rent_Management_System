from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('advertisements/<int:advertisement_id>/reviews/', views.ReviewListView.as_view(), name='advertisement-reviews'),
    path('user-reviews/', views.user_reviews_view, name='user-reviews'),
    path('my-advertisement-reviews/', views.my_advertisement_reviews_view, name='my-advertisement-reviews'),
    path('advertisements/<int:advertisement_id>/create-review/', views.create_review_view, name='create-review'),
    path('advertisements/<int:advertisement_id>/can-review/', views.can_review_view, name='can-review'),
    path('advertisements/<int:advertisement_id>/rating/', views.advertisement_rating_view, name='advertisement-rating'),
]