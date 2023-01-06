from django.urls import path

from .views import homepage, DetailPostView, search, CreatePostView

app_name = "blogs"

urlpatterns = [
    path('', homepage, name="homepage"),
    path("search/", search, name="search"),
    path("new/", CreatePostView.as_view(), name="new"),
    path('details/<int:pk>/', DetailPostView.as_view(), name='details'),
]
