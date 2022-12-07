import os
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.http import require_POST
from main.models import Post, Comment
from main.forms import EmailPostForm, CommentForm
from taggit.models import Tag
from dotenv import load_dotenv

load_dotenv()


def post_list(request, tag_slug=None):
    # Create post list to fetch all published posts
    posts = Post.published.all()
    tag = None
    if tag_slug:
        # Get post tags if there are any tag and filter using the list of tags
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    # Use paginator to split content on pages
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        # Handle page is not an integer exception
        post_list = paginator.page(1)
    except EmptyPage:
        # Handle empty page exception
        post_list = paginator.page(page_number.num_pages)
    template = "main/post_list.html"
    # Use paginated post list in the context
    context = {"post_list": post_list, "tag": tag}
    return render(request, template, context)


def post_detail(request, day, month, year, post):
    # Create post detail for seo friendly urls
    post = get_object_or_404(Post, status=Post.Status.PUBLISH, publish__day=day, publish__month=month,
                             publish__year=year, slug=post)
    # Include post comments if any and render the comment form
    comments = post.comments.filter(active=True)
    form = CommentForm()
    template = "main/post_detail.html"
    context = {"post": post, "comments": comments, "form": form}
    return render(request, template, context)


# class PostListView(ListView):
#     # Create class-based view for post list
#     queryset = Post.published.all()
#     paginate_by = 3
#     # Use context object name, if not set default is object list
#     context_object_name = "post_list"
#     template_name = "main/post_list.html"


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


@require_POST
def post_comment(request, post_pk):
    # Create post comment view and use require post to allow post request only
    post = get_object_or_404(Post, pk=post_pk, status=Post.Status.PUBLISH)
    # Set comment variable to none to indicate whether added or to render comment form
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        # Don't save until setting a post for the comment first
        comment.post = post
        comment.save()
    template = "main/post_comment.html"
    context = {"post": post, "form": form, "comment": comment}
    return render(request, template, context)
