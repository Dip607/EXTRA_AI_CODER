# forum/urls.py
  

from django.urls import path,include
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view
from django.contrib.auth.views import LogoutView
from .views import browse_public_doubts

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
    path('student/<str:username>/', views.student_profile, name='student_profile'),
    path("faculty/<str:username>/", views.faculty_profile_by_username, name="faculty_profile_by_username"),
    path('upload-doubt/', views.ocr_doubt_upload, name='ocr_doubt_upload'),
    path('browse/', browse_public_doubts, name='browse_doubts'),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/', views.resource_hub, name='resource_hub'),
    path('resources/add/', views.add_resource, name='add_resource'),
    path('resources/upvote/<int:resource_id>/', views.upvote_resource, name='upvote_resource'),
   


    
]
