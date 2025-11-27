import pytest
from django.urls import reverse, resolve
from accounts.views import (
    register, user_login, user_logout, user_home, dashboard
)


@pytest.mark.unit
class TestURLPatterns:
    """Test cases for URL patterns."""
    
    def test_home_url_resolves(self):
        """Test that home URL resolves correctly."""
        url = reverse('home')
        assert url == '/accounts/'
    
    def test_login_url_resolves(self):
        """Test that login URL resolves correctly."""
        url = reverse('login')
        assert url == '/accounts/login/'
    
    def test_register_url_resolves(self):
        """Test that register URL resolves correctly."""
        url = reverse('register')
        assert url == '/accounts/register/'
    
    def test_logout_url_resolves(self):
        """Test that logout URL resolves correctly."""
        url = reverse('logout')
        assert url == '/accounts/logout/'
    
    def test_dashboard_url_resolves(self):
        """Test that dashboard URL resolves correctly."""
        url = reverse('dashboard')
        assert url == '/accounts/dashboard/'
    
    def test_home_url_maps_to_view(self):
        """Test that home URL maps to correct view."""
        match = resolve('/')
        assert match.func == user_home
    
    def test_login_url_maps_to_view(self):
        """Test that login URL maps to correct view."""
        match = resolve('/login/')
        assert match.func == user_login
    
    def test_register_url_maps_to_view(self):
        """Test that register URL maps to correct view."""
        match = resolve('/register/')
        assert match.func == register
    
    def test_logout_url_maps_to_view(self):
        """Test that logout URL maps to correct view."""
        match = resolve('/logout/')
        assert match.func == user_logout
    
    def test_dashboard_url_maps_to_view(self):
        """Test that dashboard URL maps to correct view."""
        match = resolve('/dashboard/')
        assert match.func == dashboard
    
    def test_invalid_url_raises_404(self):
        """Test that invalid URL raises 404."""
        from django.urls import Resolver404
        with pytest.raises(Resolver404):
            resolve('/nonexistent/')
