from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    class Status(models.TextChoices):
        # Define class for post choices where Post.Status.choices obtains choices and Post.Status.labels obtains names
        DRAFT = "DF", "Draft"
        PUBLISH = "PB", "Publish"

    # Create post model and define model fields
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Use class status to set choices for post status
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    # Define many-to-one relationship with user model
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        # Order posts by publish field descendingly
        ordering = ["-publish"]
        # Add database index to optimize querying order for publish field
        indexes = [models.Index(fields=["-publish"])]

    def __str__(self):
        return self.title
