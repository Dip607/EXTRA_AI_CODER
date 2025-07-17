from django.urls import path
from . import views
app_name = 'challenges'
app_name = 'contests'
urlpatterns = [
    path('', views.contest_list, name='list'),
    path('contests/', views.contest_list, name='contest_list'),
    path('contest/<int:pk>/', views.contest_detail, name='contest_detail'),
    path('contest/create/', views.create_contest, name='create_contest'),
    path('submit/', views.submit_code, name='submit_code'),
    
]
