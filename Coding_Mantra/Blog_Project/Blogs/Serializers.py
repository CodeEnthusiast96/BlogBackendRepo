from rest_framework import serializers
from .models import Post, Comment, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'text', 'created_at']

    def get_author_name(self, obj):
        return obj.author.username if obj.author else None
    
    
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # Exclude the 'author' field from the serialized data
        fields = ['id', 'title', 'content', 'pub_date', 'author_name', 'tags', 'display_image', 'comments']

    def get_author_name(self, obj):
        return obj.author.username if obj.author else None



class MinimalPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'display_image', 'likes']