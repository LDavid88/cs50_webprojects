from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.type}"


class Listings(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    watchlist = models.ManyToManyField(User, null=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"


class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.FloatField()
    article = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="article")

    def __str__(self):
        return f"{self.bidder}"


class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.commenter}"
