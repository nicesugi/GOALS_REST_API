from django.urls import path
from posts import views


urlpatterns = [
    path("", views.PostView.as_view()),
    path("<post_id>", views.PostView.as_view()),
    path("<post_id>/existence", views.ExistencePostView.as_view()),
    path("detail/<post_id>", views.PostDetailView.as_view()),
    path("<post_id>/like", views.LikeView.as_view()),
]
