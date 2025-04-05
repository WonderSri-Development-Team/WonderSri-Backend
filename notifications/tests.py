from datetime import timezone, datetime
from django.test import TestCase, RequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from notifications.models import UserDevice
from notifications.views import check_nearby_events
from django.contrib.gis.geos import Point
from location.models import Location, Event
from django.contrib.auth.models import User
from users.models import UserProfile
from unittest.mock import patch

class NotificationTests(TestCase):
    def setUp(self):
        """ Setup for test methods """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.device = UserDevice.objects.create(user=self.user, fcm_token='test_token')
        point = Point(79.8612, 6.9271, srid=4326)  # Example coordinates for Colombo, Sri Lanka
        self.location = Location.objects.create(coordinates=point)
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event.",
            location=self.location,
            start_date=timezone.make_aware(datetime.datetime(2025, 4, 5)),
            end_date=timezone.make_aware(datetime.datetime(2025, 4, 10)),
            price=100.00,
            is_active=True,
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    @patch('notifications.views.send_push_notifications')
    def test_check_nearby_events(self, mock_send):
        """Test nearby event notification."""
        factory = RequestFactory()
        request = factory.post('/notifications/check-nearby-events/', data={
            'user_id': self.user.id,
            'latitude': 6.9271,
            'longitude': 79.8612
        }, content_type='application/json')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.access_token}'
        # request.user = self.user 

        response = check_nearby_events(request) 

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once() 

    # @patch('notifications.views.send_push_notifications')
    # def test_new_event_added_notification(self, mock_send_push_notifications):
    #     """Test new event notification (you'll likely trigger this in your Event creation logic)."""
    #     # ... (Implementation depends on how you trigger new event notifications) 
    #     pass 

    # @patch('notifications.views.send_push_notifications')
    # def test_send_general_tips(self, mock_send_push_notifications):
    #     """Test sending general tips."""
    #     send_general_tips() 
    #     self.assertGreaterEqual(mock_send_push_notifications.call_count, 1) # At least one call
    #     # You might want to add more specific assertions based on your GENERAL_TIPS

    # @patch('notifications.views.send_push_notifications')
    # def test_welcome_notification(self, mock_send_push_notifications):
    #     """Test welcome message notification."""
    #     welcome_notification(self.user)
    #     mock_send_push_notifications.assert_called_once()  

    # # Helper function to simulate sending a push notification (replace with your logic)
    # def send_push_notifications(self, fcm_token, title, body):
    #     """Mock function to simulate sending push notifications."""
    #     print(f"Sending notification to {fcm_token}: Title: {title}, Body: {body}")
    #     return True 