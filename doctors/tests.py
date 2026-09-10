from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Doctor


User = get_user_model()


class DoctorAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email="doctoruser1@example.com",
            name="Doctor User One",
            password="Password123!",
        )

        self.user2 = User.objects.create_user(
            email="doctoruser2@example.com",
            name="Doctor User Two",
            password="Password123!",
        )

        self.client.force_authenticate(user=self.user1)

    def create_doctor(self, user=None):
        return Doctor.objects.create(
            name="Dr. Amit Verma",
            specialization="Cardiology",
            contact="9876543210",
            created_by=user or self.user1,
        )

    def test_create_doctor(self):
        url = reverse("doctor-list-create")

        data = {
            "name": "Dr. Amit Verma",
            "specialization": "Cardiology",
            "contact": "9876543210",
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        doctor = Doctor.objects.first()

        self.assertEqual(
            doctor.created_by,
            self.user1,
        )

    def test_authenticated_users_can_list_doctors(self):
        self.create_doctor(self.user1)
        self.create_doctor(self.user2)

        url = reverse("doctor-list-create")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_owner_can_update_doctor(self):
        doctor = self.create_doctor(self.user1)

        url = reverse(
            "doctor-detail",
            kwargs={"pk": doctor.id},
        )

        data = {
            "name": "Dr. Amit Verma",
            "specialization": "Neurology",
            "contact": "9876543210",
        }

        response = self.client.put(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        doctor.refresh_from_db()

        self.assertEqual(
            doctor.specialization,
            "Neurology",
        )

    def test_non_owner_cannot_update_doctor(self):
        doctor = self.create_doctor(self.user1)

        self.client.force_authenticate(user=self.user2)

        url = reverse(
            "doctor-detail",
            kwargs={"pk": doctor.id},
        )

        data = {
            "name": "Hacked Doctor",
            "specialization": "Neurology",
            "contact": "1111111111",
        }

        response = self.client.put(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_non_owner_cannot_delete_doctor(self):
        doctor = self.create_doctor(self.user1)

        self.client.force_authenticate(user=self.user2)

        url = reverse(
            "doctor-detail",
            kwargs={"pk": doctor.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Doctor.objects.filter(id=doctor.id).exists()
        )