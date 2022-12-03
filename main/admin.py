from django.contrib import admin
from main.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Register post model to admin site
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    ordering = ["publish", "status"]
    autocomplete_fields = ["author"]
