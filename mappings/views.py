from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import PatientDoctorMapping
from .serializers import MappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            PatientDoctorMapping.objects
            .filter(patient__created_by=self.request.user)
            .select_related("patient", "doctor")
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save()


class MappingDetailView(generics.GenericAPIView):
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        mappings = (
            PatientDoctorMapping.objects
            .filter(
                patient_id=pk,
                patient__created_by=request.user,
            )
            .select_related("patient", "doctor")
            .order_by("-created_at")
        )

        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            mapping = PatientDoctorMapping.objects.get(
                pk=pk,
                patient__created_by=request.user,
            )
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {"detail": "Mapping not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        mapping.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )