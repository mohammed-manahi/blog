from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    # Define url patterns for post list and post detail views
    # path("", views.post_list, name="post_list"),
    path("", views.PostListView.as_view(), name="post_list"),
    # Make urls seo friendly by using date and slug combination in the post detail url
    path("<int:day>/<int:month>/<int:year>/<slug:post>/", views.post_detail, name="post_detail"),
]
