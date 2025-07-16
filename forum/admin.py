from django.contrib import admin
from .models import User, Category, Doubt, Comment

from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'added_by', 'created_at')
@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'faculty_verified', 'created_at')
    list_filter = ('faculty_verified', 'created_at')
    search_fields = ('title', 'description', 'student__username')
    list_select_related = ('student',)
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('doubt', 'author', 'created_at')
    search_fields = ('content', 'author__username', 'doubt__title')
    list_select_related = ('doubt', 'author')
    ordering = ('-created_at',)


admin.site.register(User)
admin.site.register(Category)
