from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200) 
    content = models.TextField() 
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    display_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    likes = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):      
        return f'{self.author.username} - {self.text[:50]}'    
    
    
