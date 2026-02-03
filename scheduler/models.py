from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.description} from {self.start_time} to {self.end_time}"


class Proposal(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    proponent = models.ForeignKey(User, on_delete=models.CASCADE)
    original_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="original_user_proposals"
    )
    motivation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS)
