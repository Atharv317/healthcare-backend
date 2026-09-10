from django.contrib import admin

from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "specialization",
        "contact",
        "created_by",
        "created_at",
    ]

    search_fields = [
        "name",
        "specialization",
        "contact",
    ]