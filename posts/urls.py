from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view()),
    path('<post_id>', views.PostView.as_view()),
    path('<post_id>/recover', views.RecoverPostView.as_view()),
]