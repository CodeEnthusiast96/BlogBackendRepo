from django.urls import path
from . import views
urlpatterns = [
    path('', views.BlogHome, name = "blog_home"), 
    path('detail/<int:post_id>', views.blog_detail, name = "blog_detail"), 
    path('create',views.Create, name = "create"),
    path('search',views.search_posts_by_tag, name = "search_posts_by_tag"),  
    path('comment', views.create_comment, name = "createComment"),
    path('like/<int:post_id>', views.like_post, name = "like_post")               
]