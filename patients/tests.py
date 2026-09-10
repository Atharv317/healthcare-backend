from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Patient


User = get_user_model()


class PatientAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            name="User One",
            password="Password123!",
        )

        self.user2 = User.objects.create_user(
            email="user2@example.com",
            name="User Two",
            password="Password123!",
        )

        self.client.force_authenticate(user=self.user1)

    def test_create_patient(self):
        url = reverse("patient-list-create")

        data = {
            "name": "Rahul Sharma",
            "age": 35,
            "gender": "M",
            "address": "Delhi",
            "medical_history": "Diabetes",
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Patient.objects.count(),
            1,
        )

        patient = Patient.objects.first()

        self.assertEqual(
            patient.created_by,
            self.user1,
        )

    def test_user_can_only_see_own_patients(self):
        Patient.objects.create(
            name="User 1 Patient",
            age=30,
            gender="M",
            address="Delhi",
            created_by=self.user1,
        )

        Patient.objects.create(
            name="User 2 Patient",
            age=40,
            gender="F",
            address="Mumbai",
            created_by=self.user2,
        )

        url = reverse("patient-list-create")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["name"],
            "User 1 Patient",
        )

    def test_user_cannot_access_another_users_patient(self):
        patient = Patient.objects.create(
            name="Private Patient",
            age=40,
            gender="F",
            address="Delhi",
            created_by=self.user2,
        )

        url = reverse(
            "patient-detail",
            kwargs={"pk": patient.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_create_patient(self):
        self.client.force_authenticate(user=None)

        url = reverse("patient-list-create")

        data = {
            "name": "Unauthorized Patient",
            "age": 25,
            "gender": "M",
            "address": "Delhi",
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )