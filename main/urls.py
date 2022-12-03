from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    # Define url patterns for post list and post detail views
    path("", views.post_list, name="post_list"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
]
