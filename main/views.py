import os
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError
from main.models import Post
from main.forms import EmailPostForm
from dotenv import load_dotenv

load_dotenv()


# def post_list(request):
#     # Create post list to fetch all published posts
#     posts = Post.published.all()
#     # Use paginator to split content on pages
#     paginator = Paginator(posts, 3)
#     page_number = request.GET.get("page", 1)
#     try:
#         post_list = paginator.page(page_number)
#     except PageNotAnInteger:
#         # Handle page is not an integer exception
#         post_list = paginator.page(1)
#     except EmptyPage:
#         # Handle empty page exception
#         post_list = paginator.page(page_number.num_pages)
#     template = "main/post_list.html"
#     # Use paginated post list in the context
#     context = {"post_list": post_list}
#     return render(request, template, context)


def post_detail(request, day, month, year, post):
    # Create post detail for seo friendly urls
    post = get_object_or_404(Post, status=Post.Status.PUBLISH, publish__day=day, publish__month=month,
                             publish__year=year, slug=post)
    template = "main/post_detail.html"
    context = {"post": post}
    return render(request, template, context)


class PostListView(ListView):
    # Create class-based view for post list
    queryset = Post.published.all()
    paginate_by = 3
    # Use context object name, if not set default is object list
    context_object_name = "post_list"
    template_name = "main/post_list.html"


def post_share(request, post_pk):
    # Create post share view to share recommended posts by email
    post = get_object_or_404(Post, pk=post_pk, status=Post.Status.PUBLISH)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # Build post url using get absolute url in post model
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cleaned_data['name']} recommends you read {post.title}"
            message = f"Check out {post.title} at {post_url}" + " " + \
                      f"{cleaned_data['name']}\'s comment: {cleaned_data['comment']}"
            try:
                send_mail(subject=subject, message=message, from_email=str(os.getenv("FROM_EMAIL")),
                          recipient_list=[cleaned_data["to"]])
                sent = True
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
    else:
        form = EmailPostForm()
    template = "main/post_share.html"
    context = {"form": form, "post": post, "sent": sent}
    return render(request, template, context)
