from .views import HomeView, LoginView, RegisterView, ReservationView, ReservationsView
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("reservation/", ReservationView.as_view(), name="reservation"),
    path("reservations/", ReservationsView.as_view(), name="reservations"),
]
