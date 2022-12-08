from django.contrib.sitemaps import Sitemap
from main.models import Post


class PostSitemap(Sitemap):
    # Add site map for seo optimizations
    changefreq = "weekly"
    priority = 1

    def items(self):
        # Define items for site map feeds
        return Post.published.all()

    def lastmode(self, obj):
        # Returns the last time items were updated
        return obj.updated
