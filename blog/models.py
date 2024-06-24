from django.db import models
from users.models import CustomUser
# Create your models here.

class Blog(models.Model):
    title=models.CharField(max_length=255, unique=True)
    description=models.CharField(max_length=1000)
    image=models.ImageField(upload_to='blog/images/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255, unique=True, help_text="Slug is a unique name for your blog.")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title