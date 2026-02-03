from django.contrib import admin
from .models import Reservation, Proposal


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "start_time", "end_time", "description")
    search_fields = ("user__username", "description")
    list_filter = ("start_time", "end_time")


class ProposalAdmin(admin.ModelAdmin):
    list_display = ("proponent", "reservation", "status")
    search_fields = ("proponent__username", "motivation")
    list_filter = ("status",)


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Proposal, ProposalAdmin)
