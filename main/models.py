from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    # Create custom model manager to query posts that their statuses is published
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)


class Post(models.Model):
    class Status(models.TextChoices):
        # Define class for post choices where Post.Status.choices obtains choices and Post.Status.labels obtains names
        DRAFT = "DF", "Draft"
        PUBLISH = "PB", "Publish"

    # Create post model and define model fields
    title = models.CharField(max_length=255)
    # Ensure slugs are unique by adding unique for date parameter
    slug = models.SlugField(max_length=255, unique_for_date="publish")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Use class status to set choices for post status
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    # Define many-to-one relationship with user model
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    # Default model manager, when adding custom manager it has to be explicitly defined
    objects = models.Manager()
    # Custom model manager for getting posts that their statuses is published
    published = PublishedManager()

    class Meta:
        # Order posts by publish field descendingly
        ordering = ["-publish"]
        # Add database index to optimize querying order for publish field
        indexes = [models.Index(fields=["-publish"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Define absolute url for creating canonical urls
        return reverse("main:post_detail", args=[self.publish.day, self.publish.month, self.publish.year, self.slug])
