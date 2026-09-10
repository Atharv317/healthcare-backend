from rest_framework import serializers

from .models import PatientDoctorMapping


class MappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientDoctorMapping
        fields = [
            "id",
            "patient",
            "doctor",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_patient(self, value):
        request = self.context["request"]

        if value.created_by != request.user:
            raise serializers.ValidationError(
                "You do not have permission to use this patient."
            )

        return value

    def validate(self, attrs):
        patient = attrs["patient"]
        doctor = attrs["doctor"]

        if PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor,
        ).exists():
            raise serializers.ValidationError(
                "This doctor is already assigned to this patient."
            )

        return attrs