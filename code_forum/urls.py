# code_forum/code_forum/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum.urls')),  # Include your app's URLs
]
