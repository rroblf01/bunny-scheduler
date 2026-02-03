from django.views import View
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_proposals"] = (
            Proposal.objects.filter(original_user=self.request.user)
            .select_related("reservation")
            .order_by("-id")
        )
        return context


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


class ProposalView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        reservation_id = request.POST.get("reservation_id")
        motivation = request.POST.get("motivation")
        if not reservation_id or not motivation:
            messages.error(request, "Datos incompletos para la propuesta.")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        reservation = Reservation.objects.get(id=reservation_id)

        if Proposal.objects.filter(
            reservation=reservation, proponent=request.user
        ).exists():
            messages.error(request, "Ya has realizado una propuesta para esta reserva.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        Proposal.objects.create(
            reservation=reservation,
            proponent=request.user,
            motivation=motivation,
            original_user=reservation.user,
            status="pending",
        )
        messages.success(request, "Propuesta enviada correctamente.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    def patch(self, request, *args, **kwargs):
        import json
        from django.http import JsonResponse

        try:
            data = json.loads(request.body)
            proposal_id = data.get("proposal_id")
            new_status = data.get("status")
        except Exception:
            return JsonResponse({"error": "Datos inválidos."}, status=400)
        if not proposal_id or new_status not in ["accepted", "rejected"]:
            return JsonResponse(
                {"error": "Datos inválidos para actualizar la propuesta."}, status=400
            )
        proposal = Proposal.objects.get(id=proposal_id)
        if proposal.reservation.user != request.user:
            return JsonResponse(
                {"error": "No tienes permisos para modificar esta propuesta."},
                status=403,
            )

        proposal.status = new_status
        proposal.save()
        print(proposal.status)

        if new_status == "accepted":
            print("updating reservation user")
            reservation = proposal.reservation
            reservation.user = proposal.proponent
            reservation.save()

        return JsonResponse({"success": True, "status": new_status})
