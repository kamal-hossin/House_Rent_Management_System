from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/advertisements/', views.user_advertisements_view, name='user-advertisements'),
    path('profile/rent-requests/', views.user_rent_requests_view, name='user-rent-requests'),
    path('profile/favorites/', views.user_favorites_view, name='user-favorites'),
    path('profile/reviews/', views.user_reviews_view, name='user-reviews'),
    path('verify-email/<str:token>/', views.verify_email_view, name='verify-email'),
]