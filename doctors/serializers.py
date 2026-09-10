from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "contact",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate_contact(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Contact number cannot be empty."
            )

        return value