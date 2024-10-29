from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")

    def test_user_registration_success(self):
        """Test registering a new user with valid data."""
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Test123456"
        }
        response = self.client.post(self.register_url, data, format="json")

        # Assert response status and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertIn('user', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], data['username'])
        self.assertEqual(response.data['user']['email'], data['email'])
    
    def test_user_registration_missing_field(self):
        """Test registering a user with missing required fields."""
        data = {
            "username": "testuser",
            "password": "testpassword123"
            # Missing email field
        }
        response = self.client.post(self.register_url, data)
        
        # Assert response status and data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_duplicate_username(self):
        """Test registering a user with an existing username."""
        User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123")
        data = {
            "username": "testuser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(self.register_url, data)
        
        # Assert response status and data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

class UserLoginTests(APITestCase):
    
    def setUp(self):
        self.login_url = reverse('login')
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123")
        
    def test_user_login_success(self):
        """Test logging in with valid credentials."""
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = self.client.post(self.login_url, data)
        
        # Assert response status and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_user_login_invalid_credentials(self):
        """Test logging in with invalid credentials."""
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        
        # Assert response status
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_user_login_nonexistent_user(self):
        """Test logging in with a non-existent user."""
        data = {
            "username": "nonexistent",
            "password": "somepassword"
        }
        response = self.client.post(self.login_url, data)
        
        # Assert response status
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

class TokenRefreshTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123")
        refresh = RefreshToken.for_user(self.user)
        self.valid_refresh_token = str(refresh)
        self.refresh_url = reverse('token_refresh')
        
    def test_token_refresh_success(self):
        """Test refreshing an access token with a valid refresh token."""
        data = {
            "refresh": self.valid_refresh_token
        }
        response = self.client.post(self.refresh_url, data)
        
        # Assert response status and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
    def test_token_refresh_invalid_token(self):
        """Test refreshing an access token with an invalid refresh token."""
        data = {
            "refresh": "invalidtoken123"
        }
        response = self.client.post(self.refresh_url, data)
        
        # Assert response status
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)