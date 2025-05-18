from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    full_name = models.CharField(max_length=255, unique=True)
    born_date = models.CharField(max_length=100, blank=True, null=True)
    born_location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')
    tags = models.ManyToManyField(Tag, related_name='quote')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'"{self.quote[:50]}" — {self.author.full_name}'
