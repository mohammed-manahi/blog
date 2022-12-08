from django import template
from main.models import Post

# Register new custom tag in template library
register = template.Library()


@register.simple_tag
def total_posts():
    # Register a new custom simple tag that returns a string of posts count for the template
    return Post.published.count()
