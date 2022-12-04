from django.shortcuts import render, get_object_or_404
from main.models import Post
from django.core.paginator import Paginator


def post_list(request):
    # Create post list to fetch all published posts
    posts = Post.published.all()
    # Use paginator to split content on pages
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    post_list = paginator.page(page_number)
    template = "main/post_list.html"
    # Use paginated post list in the context
    context = {"post_list": post_list}
    return render(request, template, context)


def post_detail(request, day, month, year, post):
    # Create post detail for seo friendly urls
    post = get_object_or_404(Post, status=Post.Status.PUBLISH, publish__day=day, publish__month=month,
                             publish__year=year, slug=post)
    template = "main/post_detail.html"
    context = {"post": post}
    return render(request, template, context)
