from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import ReservationForm, ProposalForm
from .models import Reservation, Proposal
from django.contrib import messages


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


class ReservationView(LoginRequiredMixin, FormView):
    template_name = "reservation.html"
    login_url = "login"
    form_class = ReservationForm

    def get_initial(self):
        initial = super().get_initial()
        date_param = self.request.GET.get("date")
        if date_param:
            initial["date"] = date_param
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        date_val = self.request.GET.get("date")
        if date_val:
            reservas = Reservation.objects.filter(start_time__date=date_val).order_by(
                "start_time"
            )
            context["reserved_hours"] = reservas
        else:
            context["reserved_hours"] = []
        return context

    def form_valid(self, form):
        from datetime import datetime

        date_val = form.cleaned_data["date"]
        start_hour = form.cleaned_data["start_hour"]
        end_hour = form.cleaned_data["end_hour"]

        start_dt = datetime.combine(date_val, start_hour)
        end_dt = datetime.combine(date_val, end_hour)

        overlap = Reservation.objects.filter(
            start_time__lt=end_dt, end_time__gt=start_dt
        ).exists()
        if overlap:
            messages.error(
                self.request,
                "No se puede reservar: ya existe una reserva en ese horario.",
            )
            return self.form_invalid(form)
        form.instance.user = self.request.user
        form.instance.start_time = start_dt
        form.instance.end_time = end_dt
        form.save()
        messages.success(self.request, "Reserva realizada correctamente.")
        return redirect("home")


class ReservationsView(LoginRequiredMixin, TemplateView):
    template_name = "reservations.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reservations"] = Reservation.objects.filter(user=self.request.user)
        return context


class ProposalView(LoginRequiredMixin, TemplateView):
    template_name = "proposal.html"
    login_url = "login"
    form_class = ProposalForm
