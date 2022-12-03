from django.shortcuts import render, get_object_or_404
from main.models import Post


def post_list(request):
    # Create post list to fetch all published posts
    posts = Post.published.all()
    template = "main/post_list.html"
    context = {"posts": posts}
    return render(request, template, context)


def post_detail(request, pk):
    # Create post detail to fetch a post by its pk
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISH)
    template = "main/post_detail.html"
    context = {"post": post}
    return render(request, template, context)
