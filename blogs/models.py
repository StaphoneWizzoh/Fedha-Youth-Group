from datetime import datetime
from django.db import models
from django.utils import timezone
from members.models import Registration


class Category(models.Model):
    title = models.CharField(max_length=20)
    post_count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=20)
    post_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=50)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Registration, on_delete=models.CASCADE)
    thumbnail = models.ImageField(null=True, blank=True, upload_to="blogs/photos/")
    categories = models.ManyToManyField(Category, default=None)
    tags = models.ManyToManyField(Tag, default=None)

    def __str__(self):
        return self.title

    @property
    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
