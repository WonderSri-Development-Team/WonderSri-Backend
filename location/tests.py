from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Event, Activity, Food
from users.models import UserProfile

User = get_user_model()

class LocationViewsTest(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        # Create sample data
        self.event = Event.objects.create(
            title='Sample Event',
            description='This is a sample event.',
            start_date='2025-03-01T18:00:00Z',
            end_date='2025-03-01T21:00:00Z',
            price=20.00
        )
        self.activity = Activity.objects.create(
            title='Sample Activity',
            description='This is a sample activity.',
            location=self.event.location  # Assuming the event has a location
        )
        self.food = Food.objects.create(
            food_name='Sample Food'
        )

    def test_list_nearby_events(self):
        url = reverse('list_nearby_events')  # Adjust the name as per your URL configuration
        response = self.client.get(url, {'lat': 0, 'lon': 0, 'radius': 2000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_create_event(self):
        url = reverse('create_event')  # Adjust the name as per your URL configuration
        data = {
            'title': 'New Event',
            'description': 'A new event description.',
            'start_date': '2025-03-10T18:00:00Z',
            'end_date': '2025-03-10T21:00:00Z',
            'price': 25.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)  # Check if the event count increased

    def test_update_event(self):
        url = reverse('update_event', args=[self.event.pk])  # Adjust the name as per your URL configuration
        data = {
            'title': 'Updated Event',
            'description': 'Updated description.',
            'start_date': '2025-03-01T19:00:00Z',
            'end_date': '2025-03-01T22:00:00Z',
            'price': 30.00
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event')

    def test_delete_event(self):
        url = reverse('delete_event', args=[self.event.pk])  # Adjust the name as per your URL configuration
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)  # Check if the event was deleted

    def test_list_nearby_activities(self):
        url = reverse('list_nearby_activities')  # Adjust the name as per your URL configuration
        response = self.client.get(url, {'lat': 0, 'lon': 0, 'radius': 2000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_create_activity(self):
        url = reverse('create_activity')  # Adjust the name as per your URL configuration
        data = {
            'title': 'New Activity',
            'description': 'A new activity description.',
            'location': self.event.location.pk  # Assuming the event has a location
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 2)  # Check if the activity count increased

    def test_update_activity(self):
        url = reverse('update_activity', args=[self.activity.pk])  # Adjust the name as per your URL configuration
        data = {
            'title': 'Updated Activity',
            'description': 'Updated description.',
            'location': self.event.location.pk  # Assuming the event has a location
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.title, 'Updated Activity')

    def test_delete_activity(self):
        url = reverse('delete_activity', args=[self.activity.pk])  # Adjust the name as per your URL configuration
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Activity.objects.count(), 0)  # Check if the activity was deleted

    def test_create_food(self):
        url = reverse('create_food')  # Adjust the name as per your URL configuration
        data = {
            'food_name': 'New Food'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Food.objects.count(), 2)  # Check if the food count increased

    def test_list_food(self):
        url = reverse('list_food')  # Adjust the name as per your URL configuration
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_update_food(self):
        url = reverse('update_food', args=[self.food.pk])  # Adjust the name as per your URL configuration
        data = {
            'food_name': 'Updated Food'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.food.refresh_from_db()
        self.assertEqual(self.food.food_name, 'Updated Food')

    def test_delete_food(self):
        url = reverse('delete_food', args=[self.food.pk])  # Adjust the name as per your URL configuration
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Food.objects.count(), 0)  # Check if the food was deleted

    def test_update_profile_picture(self):
        url = reverse('update_profile_picture')  # Adjust the name as per your URL configuration
        data = {
            'profile_picture': 'path/to/image.jpg'  # Use a valid image path or mock the upload
        }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile(self):
        url = reverse('get_profile')  # Adjust the name as per your URL configuration
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.username)

