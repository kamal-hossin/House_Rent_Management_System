from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('manage-advertisements/', views.manage_advertisements, name='manage-advertisements'),
    path('manage-users/', views.manage_users, name='manage-users'),
    path('manage-categories/', views.manage_categories, name='manage-categories'),
]