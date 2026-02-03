from .views import HomeView, LoginView, RegisterView
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
