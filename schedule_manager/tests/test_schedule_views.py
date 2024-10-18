from django.urls import reverse
from rest_framework import status
from schedule_manager.models import Schedule
from rest_framework.test import APITestCase, APIClient
from schedule_manager.tests.factories import UserFactory
from schedule_manager.serializers import ScheduleSerializer


class ScheduleEndpointsTestCases(APITestCase):
    """Schedule endpoint test case."""

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.url = reverse('schedule-list')

    def test_create_schedule_with_camera_ids_unathenticated_user(self):
        """Test create schedule with unauthenticated user."""
        payload = {
            "day": "monday",
            "start": "00:00",
            "stop": "01:00",
            "camera_ids": [1, 2, 3]
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_schedule_with_camera_ids_authenticated_user(self):
        """Test create schedule with authenticated user."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "day": "monday",
            "start": "00:00",
            "stop": "01:00",
            "camera_ids": [1, 2, 3]
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create again with the same payload
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], "Schedule with these IDs already exists.")

    def test_create_schedule_with_camera_ids_and_badge_ids_authenticated_user(self):
        """Test create schedule both camera and badge ids exist."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "day": "monday",
            "start": "00:00",
            "stop": "01:00",
            "camera_ids": [1, 2, 3],
            "badge_ids": [1, 2, 3]
        }

        response = self.client.post(self.url, payload, format='json')
        expected_response = "You can provide either 'badge_ids' or 'camera_ids', not both."
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], expected_response)

    def test_create_schedule_with_camera_ids_then_update_authenticated_user(self):
        """Test create schedule with authenticated user and then update it with badge ids."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "day": "monday",
            "start": "00:00",
            "stop": "01:00",
            "camera_ids": [1, 2, 3]
        }

        response = self.client.post(self.url, payload, format='json')
        data = ScheduleSerializer(Schedule.objects.latest('created_at')).data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # badge and camera shouldn't exist together
        latest_creted_schedule = Schedule.objects.latest('created_at')
        url = reverse('schedule-detail', kwargs={'pk': latest_creted_schedule.id})
        payload = {
            "day": "monday",
            "start": "00:00",
            "stop": "01:00",
            "badge_ids": [1, 2, 3]
        }
        response = self.client.patch(url, payload, format='json')
        expected_response = "Cannot include badge IDs without removing existing camera IDs."
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], expected_response)

    def test_create_schedule_with_camera_ids_then_update_again_authenticated_user(self):
        """Test create schedule with authenticated user and then update it with badge ids."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "day": "monday",
            "start": "00:00",
            "stop": "01:00",
            "badge_ids": [1, 2, 3]
        }

        response = self.client.post(self.url, payload, format='json')
        data = ScheduleSerializer(Schedule.objects.latest('created_at')).data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create again with different payload then update to matched the existing data
        payload = {
            "day": "monday",
            "start": "00:00",
            "stop": "01:00",
            "badge_ids": [1, 2, 3, 4]
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # This payload should be matched with the existing data
        latest_creted_schedule = Schedule.objects.latest('created_at')
        payload = {
            "day": "monday",
            "start": "00:00",
            "stop": "01:00",
            "badge_ids": [1, 2, 3]
        }

        reverse_url = reverse('schedule-detail', kwargs={'pk': latest_creted_schedule.id})
        response = self.client.patch(reverse_url, payload, format='json')

        # badge and camera shouldn't exist together
        latest_creted_schedule = Schedule.objects.latest('created_at')
        reverse_url = reverse('schedule-detail', kwargs={'pk': latest_creted_schedule.id})
        payload = {
            "day": "monday",
            "start": "00:00",
            "stop": "01:00",
            "camera_ids": [1, 2, 3]
        }
        response = self.client.patch(reverse_url, payload, format='json')
        expected_response = "Cannot include camera IDs without removing existing badge IDs."
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], expected_response)
