from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "address",
            "medical_history",
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

    def validate_age(self, value):
        if value > 150 or value < 0:
            raise serializers.ValidationError(
                "Please provide a valid age."
            )

        return value