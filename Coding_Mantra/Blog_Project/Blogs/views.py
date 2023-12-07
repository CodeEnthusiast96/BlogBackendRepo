from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .Serializers import PostSerializer, MinimalPostSerializer, CommentSerializer
from django.contrib.auth.models import User
from Blogs.models import Tag
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.pagination import PageNumberPagination

from django.db.models import Prefetch
from django.http import JsonResponse


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'   
    max_page_size = 100


@api_view(['GET'])
def BlogHome(request):
    if request.method == 'GET':    
        # Retrieve all posts
        posts = Post.objects.all()

        # Use pagination
        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(posts, request)

        # Serialize the posts using the MinimalPostSerializer
        serializer = MinimalPostSerializer(result_page, many=True)

        # Return the paginated serialized data
        return paginator.get_paginated_response(serializer.data)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def Create(request):
    if request.method == 'POST':
        # Extract data from the request
        title = request.data.get('title', '')
        content = request.data.get('content', '')    
        author_id = request.data.get('author', None)
        tags = request.data.get('tags', [])
        display_image = request.FILES.get('display_image', None)
        
        # Validate data      
        if not title or not content or not author_id:
            return Response({'error': 'Title, content, and author are required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the User object for the author
            author_obj = User.objects.get(id=author_id)
        except ObjectDoesNotExist:   
            return Response({'error': 'Author does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Post instance
        post_data = {
            'title': title,
            'content': content,
            'author': author_obj,
            'display_image': display_image,  
        }

        try:
            post = Post.objects.create(**post_data)
        except Exception as e:
            return Response({'error': f'Error creating post: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Add tags to the post
        if tags:
            tag_objects = Tag.objects.filter(id__in=tags)
            post.tags.set(tag_objects)

        # Serialize the created post
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)     




@api_view(['GET'])
def search_posts_by_tag(request):
    tag_name = request.GET.get('tag_name', '')

    if not tag_name:
        return JsonResponse({'error': 'Tag name is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Using prefetch_related to fetch related posts in a single query
        tag = Tag.objects.prefetch_related(Prefetch('posts', queryset=Post.objects.only('id', 'title', 'display_image')))
        tag = tag.get(name=tag_name)

        # Accessing the pre-fetched posts
        posts = tag.posts.all()    

        serializer = MinimalPostSerializer(posts, many=True)

        return JsonResponse({'results': serializer.data}, status=status.HTTP_200_OK)
    except Tag.DoesNotExist:
        return JsonResponse({'error': f'Tag with name {tag_name} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['POST'])
def create_comment(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def like_post(request, post_id):

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': f'Post with id {post_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    post.likes += 1
    post.save()

    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def blog_detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': f'Post with id {post_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post)

    return Response(serializer.data, status=status.HTTP_200_OK)