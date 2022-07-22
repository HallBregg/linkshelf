from django.db import models


class Tag(models.Model):
    name = models.TextField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tag'


class Bookmark(models.Model):
    url = models.URLField(unique=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookmark'
