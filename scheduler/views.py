from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    login_url = "login"


class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = "/"

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(self.get_success_url())


class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())
