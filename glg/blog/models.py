from django.db import models
from django.utils import timezone

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="display_image/")
    image_description = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date="created")
    content = models.TextField(max_length=60_000)
    created = models.DateTimeField(auto_now_add = True)
    
    
    class Meta:
        ordering = ("-created",)
        permissions = [
            ("post", "Can change add a blog"),
            ("edit", "Can edit a blog"),
            ("delete", "Can delete a blog"),
        ]

    def __str__(self):
        return self.title

