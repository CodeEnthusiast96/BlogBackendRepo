from django.contrib import admin
from .models import Tag, Post, Comment

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date',)
    list_filter = ('author', 'pub_date',)
    search_fields = ('title', 'content', 'author__username',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at',)
    list_filter = ('post', 'author', 'created_at',)
    search_fields = ('post__title', 'author__username', 'text',)
