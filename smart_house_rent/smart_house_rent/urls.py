"""
URL configuration for smart_house_rent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart House Rent Management System</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; text-align: center; }
            .api-endpoints { margin-top: 30px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #007bff; }
        </style>
    </head>
    <body>
        <h1>🏠 Smart House Rent Management System</h1>
        <p style="text-align: center; color: #666;">Django REST API Server is running successfully!</p>
        
        <div class="api-endpoints">
            <h2>Available API Endpoints:</h2>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>Admin Panel:</strong> <a href="/admin-panel/">/admin-panel/</a>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>Django Admin:</strong> <a href="/admin/">/admin/</a>
            </div>
            
            <div class="endpoint">
                <span class="method">API</span> <strong>Users:</strong> /api/users/
            </div>
            
            <div class="endpoint">
                <span class="method">API</span> <strong>Advertisements:</strong> /api/advertisements/
            </div>
            
            <div class="endpoint">
                <span class="method">API</span> <strong>Rent Requests:</strong> /api/rent-requests/
            </div>
            
            <div class="endpoint">
                <span class="method">API</span> <strong>Favorites:</strong> /api/favorites/
            </div>
            
            <div class="endpoint">
                <span class="method">API</span> <strong>Reviews:</strong> /api/reviews/
            </div>
        </div>
        
        <p style="text-align: center; margin-top: 40px; color: #888; font-size: 14px;">
            Server Status: ✅ Running | Django 6.0.1 | Development Mode
        </p>
    </body>
    </html>
    """)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # Admin panel URLs
    path('admin-panel/', include('admin_panel.urls')),
    
    # API URLs
    path('api/users/', include('users.urls')),
    path('api/advertisements/', include('advertisements.urls')),
    path('api/rent-requests/', include('rent_requests.urls')),
    path('api/favorites/', include('favorites.urls')),
    path('api/reviews/', include('reviews.urls')),
]
