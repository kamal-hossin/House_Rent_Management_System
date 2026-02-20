from django.urls import path
from . import views

urlpatterns = [
    path('favorites/', views.FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/<int:pk>/', views.FavoriteDetailView.as_view(), name='favorite-detail'),
    path('user-favorites/', views.user_favorites_view, name='user-favorites'),
    path('add-favorite/', views.add_favorite_view, name='add-favorite'),
    path('remove-favorite/<int:advertisement_id>/', views.remove_favorite_view, name='remove-favorite'),
    path('is-favorite/<int:advertisement_id>/', views.is_favorite_view, name='is-favorite'),
    path('favorites-count/', views.favorites_count_view, name='favorites-count'),
]