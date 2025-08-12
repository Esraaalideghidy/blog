from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content=models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    img=models.ImageField(upload_to='blog-image/')
    tags=TaggableManager()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detailed_blog", kwargs={"pk": self.pk})
    def get_related_posts_by_tags(self):
        related_blogs = Blog.objects.filter(tags__in=self.tags.all()).distinct()
        return related_blogs

    
    

class Comment(models.Model):
    content=models.CharField(max_length=500)
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment_count')
    active=models.BooleanField(default=True)
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.user.username}'
    


class About(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    img=models.ImageField(upload_to='about/')
    background=models.TextField()
    teamwork=models.TextField()
    our_core_value=models.TextField()
    def __str__(self):
        return self.title   
    
class ContactInfo(models.Model):
    map=models.CharField(max_length=500)
    address=models.CharField(max_length=250)
    phone=models.CharField(max_length=20)
    email=models.EmailField()
    facebook=models.CharField(max_length=50)
    twitter=models.CharField(max_length=50)
    youtube=models.CharField(max_length=50)
    instagram=models.CharField(max_length=50)

class ContactUs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.user.username



   



