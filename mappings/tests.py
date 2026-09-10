from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from doctors.models import Doctor
from patients.models import Patient

from .models import PatientDoctorMapping


User = get_user_model()


class MappingAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email="mappinguser1@example.com",
            name="Mapping User One",
            password="Password123!",
        )

        self.user2 = User.objects.create_user(
            email="mappinguser2@example.com",
            name="Mapping User Two",
            password="Password123!",
        )

        self.patient1 = Patient.objects.create(
            name="Patient One",
            age=30,
            gender="M",
            address="Delhi",
            created_by=self.user1,
        )

        self.patient2 = Patient.objects.create(
            name="Patient Two",
            age=40,
            gender="F",
            address="Mumbai",
            created_by=self.user2,
        )

        self.doctor1 = Doctor.objects.create(
            name="Dr. Amit Verma",
            specialization="Cardiology",
            contact="9876543210",
            created_by=self.user1,
        )

        self.doctor2 = Doctor.objects.create(
            name="Dr. Neha Sharma",
            specialization="Neurology",
            contact="9876543211",
            created_by=self.user2,
        )

        self.client.force_authenticate(user=self.user1)

    def test_create_mapping(self):
        url = reverse("mapping-list-create")

        data = {
            "patient": self.patient1.id,
            "doctor": self.doctor1.id,
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            PatientDoctorMapping.objects.filter(
                patient=self.patient1,
                doctor=self.doctor1,
            ).exists()
        )

    def test_duplicate_mapping_is_rejected(self):
        PatientDoctorMapping.objects.create(
            patient=self.patient1,
            doctor=self.doctor1,
        )

        url = reverse("mapping-list-create")

        data = {
            "patient": self.patient1.id,
            "doctor": self.doctor1.id,
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_user_cannot_map_another_users_patient(self):
        url = reverse("mapping-list-create")

        data = {
            "patient": self.patient2.id,
            "doctor": self.doctor1.id,
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            PatientDoctorMapping.objects.filter(
                patient=self.patient2,
                doctor=self.doctor1,
            ).exists()
        )

    def test_user_can_get_own_patient_mappings(self):
        PatientDoctorMapping.objects.create(
            patient=self.patient1,
            doctor=self.doctor1,
        )

        url = reverse(
            "mapping-detail",
            kwargs={"pk": self.patient1.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_user_cannot_get_another_users_patient_mappings(self):
        PatientDoctorMapping.objects.create(
            patient=self.patient2,
            doctor=self.doctor2,
        )

        url = reverse(
            "mapping-detail",
            kwargs={"pk": self.patient2.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            0,
        )

    def test_delete_mapping(self):
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient1,
            doctor=self.doctor1,
        )

        url = reverse(
            "mapping-detail",
            kwargs={"pk": mapping.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            PatientDoctorMapping.objects.filter(
                id=mapping.id
            ).exists()
        )