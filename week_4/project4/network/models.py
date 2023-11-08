from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    post = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} on {self.date}"
