from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path('login', TokenObtainPairView.as_view()),
]