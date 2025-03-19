from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse


class UserViewTest(APITestCase):
    def setUp(self):
        # Set up the test client
        self.client = APIClient()

        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.test_user.is_active = True
        self.test_user.save()

        # Obtain JWT tokens
        refresh = RefreshToken.for_user(self.test_user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_signup(self):
        """Test user signup."""
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword23456',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # One existing user from setUp
        self.assertEqual(response.data['user']['username'], data['username'])
        self.assertEqual(response.data['user']['email'], data['email'])
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_signup_existing_username(self):
        """Test signup with an existing username."""
        url = reverse('signup')
        data = {
            'username': 'testuser',  # Already exists
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_signup_existing_email(self):
        """Test signup with an existing email."""
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'email': 'testuser@example.com',  # Already exists
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_login_success(self):
        """Test successful user login."""
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_missing_credentials(self):
        """Test login with missing credentials."""
        url = reverse('login')
        data = {'email': 'testuser@example.com'}  # Missing password
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        data = {'password': 'testpassword'}  # Missing email
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_test_auth_authenticated(self):
        """Test the test_auth endpoint with a logged-in user."""
        url = reverse('test-auth')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'Authenticated as {self.test_user.username}')

    def test_logout(self):
        """Test user logout."""
        refresh = RefreshToken.for_user(self.test_user)
        url = reverse('logout')
        data = {'refresh_token': str(refresh)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')

    def test_change_username(self):
        """Test changing the username of a logged-in user."""
        url = reverse('change-username')
        data = {'username': 'updatedusername'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Username changed successfully.')

        # Check if the username actually updated in the database
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, 'updatedusername')

    def test_request_password_reset(self):
        """Test requesting a password reset."""
        url = reverse('request-password-reset')
        data = {'email': 'testuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password reset link sent to your email')

    def test_reset_password(self):
        """Test resetting the password using a valid token."""

        # Generate a password reset token for the test user
        token = default_token_generator.make_token(self.test_user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.test_user.pk))

        # Construct the password reset URL
        url = reverse('reset-password', kwargs={'uidb64': uidb64, 'token': token})

        data = {'password': 'newpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password reset successful')

        # Verify that the password has been updated
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password('newpassword'))

    def test_change_password(self):
        """Test changing the password of a logged-in user."""
        url = reverse('change-password')
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password updated successfully')

        # Verify the password change
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password('newpassword123'))

    def test_change_email(self):
        """Test changing the email of a logged-in user."""
        url = reverse('change-email')
        new_email = 'newemail@example.com'
        data = {'email': new_email}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Email changed successfully')

        # Refresh the user from the database and check the email
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.email, new_email)

    def test_delete_account(self):
        """Test deleting the account of a logged-in user."""
        url = reverse('delete-account')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the user was deleted
        self.assertFalse(User.objects.filter(pk=self.test_user.pk).exists())
