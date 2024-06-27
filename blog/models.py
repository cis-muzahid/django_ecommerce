from django.db import models
from users.models import CustomUser
# Create your models here.
class BlogCategory(models.Model):
    name = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title=models.CharField(max_length=255, unique=True)
    description=models.CharField(max_length=1000)
    image=models.ImageField(upload_to='blog/images/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255, unique=True, help_text="Slug is a unique name for your blog.")
    category = models.ForeignKey(BlogCategory, null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    description=models.CharField(max_length=500)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
