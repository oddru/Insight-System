import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from tests.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.integration
class TestViews:
    """Test cases for views."""
    
    def setup_method(self):
        """Set up test client before each test."""
        self.client = Client()
    
    def test_user_home_view_get(self):
        """Test GET request to home view."""
        response = self.client.get(reverse('home'))
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_register_view_get(self):
        """Test GET request to register view."""
        response = self.client.get(reverse('register'))
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_register_view_post_valid_data(self):
        """Test POST request to register with valid data."""
        response = self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        assert response.status_code == 302  # Redirect on success
        assert User.objects.filter(email='newuser@example.com').exists()
    
    def test_register_view_post_creates_user(self):
        """Test that registering creates a new user."""
        initial_count = User.objects.count()
        self.client.post(reverse('register'), {
            'email': 'testuser@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        })
        assert User.objects.count() > initial_count
    
    def test_register_view_redirects_to_dashboard(self):
        """Test that successful registration redirects to dashboard."""
        response = self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }, follow=False)
        assert response.status_code == 302
        assert reverse('dashboard') in response.url
    
    def test_login_view_get(self):
        """Test GET request to login view."""
        response = self.client.get(reverse('login'))
        assert response.status_code == 200
    
    def test_login_view_post_valid_credentials(self):
        """Test POST request to login with valid credentials."""
        user = UserFactory()
        response = self.client.post(reverse('login'), {
            'username': user.username,
            'password': 'testpass123!'
        })
        assert response.status_code == 302
    
    def test_login_view_post_invalid_credentials(self):
        """Test POST request to login with invalid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'nonexistent',
            'password': 'wrongpass'
        })
        assert response.status_code == 200
        assert 'error_message' in response.context
    
    def test_login_view_error_message(self):
        """Test error message is displayed on failed login."""
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        assert 'No account detected' in response.content.decode()
    
    def test_dashboard_requires_authentication(self):
        """Test that dashboard requires authentication."""
        response = self.client.get(reverse('dashboard'))
        assert response.status_code == 302  # Redirect to home
    
    def test_dashboard_authenticated_user(self):
        """Test that authenticated user can access dashboard."""
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('dashboard'))
        assert response.status_code == 200
    
    def test_logout_view(self):
        """Test logout view."""
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('logout'))
        assert response.status_code == 302
    
    def test_logout_removes_session(self):
        """Test that logout removes user session."""
        user = UserFactory()
        self.client.force_login(user)
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('dashboard'))
        assert response.status_code == 302  # Should redirect, user not authenticated
    
    @pytest.mark.slow
    def test_multiple_login_attempts(self):
        """Test multiple login attempts."""
        for i in range(3):
            response = self.client.post(reverse('login'), {
                'username': f'user{i}',
                'password': 'wrongpass'
            })
            assert response.status_code == 200
