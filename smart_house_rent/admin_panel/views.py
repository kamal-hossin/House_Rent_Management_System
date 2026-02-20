from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from advertisements.models import Advertisement, Category
from users.models import User
from rent_requests.models import RentRequest
from reviews.models import Review

@staff_member_required
def admin_dashboard(request):
    # Statistics
    total_users = User.objects.count()
    total_advertisements = Advertisement.objects.count()
    approved_advertisements = Advertisement.objects.filter(status='approved').count()
    pending_advertisements = Advertisement.objects.filter(status='pending').count()
    rented_advertisements = Advertisement.objects.filter(status='rented').count()
    
    total_rent_requests = RentRequest.objects.count()
    pending_requests = RentRequest.objects.filter(status='pending').count()
    
    total_reviews = Review.objects.count()
    avg_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    # Recent activity
    recent_users = User.objects.order_by('-created_at')[:10]
    recent_advertisements = Advertisement.objects.order_by('-created_at')[:10]
    recent_requests = RentRequest.objects.order_by('-created_at')[:10]
    
    # Monthly statistics
    last_6_months = []
    for i in range(6):
        month_start = timezone.now().replace(day=1) - timedelta(days=i*30)
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        
        users_count = User.objects.filter(created_at__gte=month_start, created_at__lt=month_end).count()
        ads_count = Advertisement.objects.filter(created_at__gte=month_start, created_at__lt=month_end).count()
        
        last_6_months.append({
            'month': month_start.strftime('%B %Y'),
            'users': users_count,
            'advertisements': ads_count
        })
    
    context = {
        'total_users': total_users,
        'total_advertisements': total_advertisements,
        'approved_advertisements': approved_advertisements,
        'pending_advertisements': pending_advertisements,
        'rented_advertisements': rented_advertisements,
        'total_rent_requests': total_rent_requests,
        'pending_requests': pending_requests,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 2),
        'recent_users': recent_users,
        'recent_advertisements': recent_advertisements,
        'recent_requests': recent_requests,
        'last_6_months': reversed(last_6_months),
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

@staff_member_required
def manage_advertisements(request):
    advertisements = Advertisement.objects.all().select_related('owner', 'category')
    return render(request, 'admin_panel/manage_advertisements.html', {'advertisements': advertisements})

@staff_member_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin_panel/manage_users.html', {'users': users})

@staff_member_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/manage_categories.html', {'categories': categories})