from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.FloatField()

    def __str__(self):
        return f"{self.bid}"


class Comment(models.Model):
    pass


class Category(models.Model):
    type = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.type}"


class Listing(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    actual_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="actualBid")
    image = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

