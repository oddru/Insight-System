import pytest
from django.test import Client
from tests.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.integration
class TestAuthenticationFlow:
    """Integration tests for authentication flow."""
    
    def setup_method(self):
        """Set up test client before each test."""
        self.client = Client()
    
    def test_complete_registration_flow(self):
        """Test complete registration flow."""
        # Register a new user
        response = self.client.post('/register/', {
            'email': 'integration@example.com',
            'password1': 'IntegrationPass123!',
            'password2': 'IntegrationPass123!'
        })
        
        assert response.status_code == 302
        
        # Try to login with new user
        response = self.client.post('/login/', {
            'username': 'integration@example.com',
            'password': 'IntegrationPass123!'
        })
        
        assert response.status_code == 302
    
    def test_login_and_dashboard_access(self):
        """Test login and dashboard access flow."""
        # Create a user
        user = UserFactory(username='testuser', email='test@example.com')
        
        # Login
        login_success = self.client.login(
            username='testuser',
            password='testpass123!'
        )
        assert login_success
        
        # Access dashboard
        response = self.client.get('/dashboard/')
        assert response.status_code == 200
    
    def test_logout_flow(self):
        """Test logout flow."""
        user = UserFactory()
        self.client.force_login(user)
        
        # Verify user is logged in
        response = self.client.get('/dashboard/')
        assert response.status_code == 200
        
        # Logout
        response = self.client.post('/logout/')
        assert response.status_code == 302
        
        # Try to access dashboard
        response = self.client.get('/dashboard/')
        assert response.status_code == 302
    
    def test_duplicate_email_registration_fails(self):
        """Test that duplicate email registration fails."""
        # Create first user
        UserFactory(email='duplicate@example.com')
        
        # Try to register with same email
        response = self.client.post('/register/', {
            'email': 'duplicate@example.com',
            'password1': 'Pass123!',
            'password2': 'Pass123!'
        })
        
        assert response.status_code == 200  # Form re-rendered with errors
