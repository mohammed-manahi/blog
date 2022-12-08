from django import template
from main.models import Post

# Register new custom tag in template library
register = template.Library()


@register.simple_tag
def total_posts():
    # Register a new custom simple tag that returns a string of posts count for the template
    return Post.published.count()


@register.inclusion_tag("main/latest_posts.html")
def latest_posts(count=5):
    # Register a new custom inclusion tag that renders a dictionary of values for the template of the latest posts
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}
