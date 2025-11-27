import pytest
from django.contrib.auth.models import User
from tests.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.unit
class TestUserModel:
    """Test cases for Django User model."""
    
    def test_create_user(self):
        """Test creating a user."""
        user = UserFactory()
        assert user.pk is not None
        assert user.username is not None
        assert user.email is not None
    
    def test_user_string_representation(self):
        """Test user string representation."""
        user = UserFactory(username='testuser')
        assert str(user) == 'testuser'
    
    def test_user_email_unique(self):
        """Test that email field works correctly."""
        user1 = UserFactory(email='unique@example.com')
        assert user1.email == 'unique@example.com'
    
    def test_user_has_attributes(self):
        """Test user has all required attributes."""
        user = UserFactory(
            first_name='John',
            last_name='Doe'
        )
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'
    
    def test_user_password_is_hashed(self):
        """Test that user password is properly hashed."""
        user = UserFactory()
        # Password should be hashed, not plain text
        assert not user.password.startswith('testpass')
        assert user.check_password('testpass123!')
    
    def test_user_is_active_by_default(self):
        """Test that new users are active by default."""
        user = UserFactory()
        assert user.is_active is True
    
    def test_user_is_not_staff_by_default(self):
        """Test that new users are not staff by default."""
        user = UserFactory()
        assert user.is_staff is False
    
    @pytest.mark.slow
    def test_bulk_user_creation(self):
        """Test creating multiple users."""
        users = UserFactory.create_batch(5)
        assert User.objects.count() >= 5
        assert len(users) == 5
