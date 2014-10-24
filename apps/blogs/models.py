from django.db import models
from django.conf import settings
from common.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True, null=True)

    def __str__(self):
        return self.title
