import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from main.models import Post

# Register new custom tag in template library
register = template.Library()


@register.simple_tag
def get_total_posts():
    # Register a new custom simple tag that returns a string of posts count for the template
    return Post.published.count()


@register.simple_tag
def get_most_commented_posts(count=3):
    # Register a new custom simple tag that returns the most commented posts
    return Post.published.annotate(total_comments=Count("comments")).order_by("-total_comments")[:count]


@register.inclusion_tag("main/latest_posts.html")
def get_latest_posts(count=5):
    # Register a new custom inclusion tag that renders a dictionary of values for the template of the latest posts
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.filter(name="markdown")
def markdown_format(text):
    # Register a new custom filter for markdown typing
    return mark_safe(markdown.markdown(text))