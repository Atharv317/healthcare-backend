from django.db import models
from django.conf import settings


class Patient(models.Model):

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    name = models.CharField(max_length=150)

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
    )

    address = models.TextField()

    medical_history = models.TextField(
        blank=True,
        default="",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patients",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name