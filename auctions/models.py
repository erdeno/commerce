from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist_item_count = models.IntegerField()


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    category_name = models.CharField(max_length=64)
    item_count = models.IntegerField()

    def __str__(self):
        return f"{self.category_name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="listing_category",
        null=True,
        blank=True,
    )
    description = models.TextField()
    image_url = models.CharField(max_length=500)
    starting_price = models.IntegerField()
    current_price = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date = models.DateTimeField(auto_now_add=True)
    watchers = models.ManyToManyField(User, related_name="watchers", blank=True)
    is_active = models.BooleanField(default=True)
    last_bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="last_bid",
        blank=True,
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_amount = models.IntegerField()
    bid_item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bid_item"
    )

    def __str__(self):
        return f"${self.bid_amount} bid from {self.bidder} to {self.bid_item}"


class Comment(models.Model):
    comment_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user", null=True
    )
    comment_item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comment_item", null=True
    )
    title = models.CharField(max_length=64)
    content = models.TextField()
    rate = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment from {self.comment_user} to {self.comment_item} on {self.date.day}/{self.date.month}/{self.date.year}"
