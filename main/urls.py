from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    # Define url patterns for post list and post detail views
    path("", views.post_list, name="post_list"),
    # Define tag url
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path("", views.PostListView.as_view(), name="post_list"),
    # Make urls seo friendly by using date and slug combination in the post detail url
    path("<int:day>/<int:month>/<int:year>/<slug:post>/", views.post_detail, name="post_detail"),
    # Define post share url
    path("<int:post_pk>/share/", views.post_share, name="post_share"),
    # Define post comment url
    path("<int:post_pk>/comment/", views.post_comment, name="post_comment"),

]
