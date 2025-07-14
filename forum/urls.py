# forum/urls.py

from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'), 
    path('ask/', views.ask_doubt, name='ask_doubt'),
    path('doubt/<int:doubt_id>/', views.view_doubt, name='view_doubt'),
    path('verify/<int:doubt_id>/', views.verify_doubt, name='verify_doubt'),
    path('login/', auth_views.LoginView.as_view(template_name='forum/login.html'), name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/success/', views.logout_success, name='logout_success'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('notifications/unread_count/', views.unread_notification_count, name='unread_notification_count'),
    
]
