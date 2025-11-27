import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.forms import CustomUserCreationForm
from tests.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.unit
class TestCustomUserCreationForm:
    """Test cases for CustomUserCreationForm."""
    
    def test_form_valid_data(self):
        """Test form is valid with correct data."""
        form_data = {
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
    
    def test_form_invalid_mismatched_passwords(self):
        """Test form is invalid when passwords don't match."""
        form_data = {
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'password2' in form.errors
    
    def test_form_invalid_duplicate_email(self):
        """Test form is invalid when email already exists."""
        UserFactory(email='existing@example.com')
        form_data = {
            'email': 'existing@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors
    
    def test_form_invalid_weak_password(self):
        """Test form is invalid with weak password."""
        form_data = {
            'email': 'newuser@example.com',
            'password1': '123',
            'password2': '123'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
    
    def test_form_save_creates_user(self):
        """Test that form.save() creates a user."""
        form_data = {
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.pk is not None
        assert user.username == 'newuser@example.com'
        assert user.email == 'newuser@example.com'
    
    def test_form_email_used_as_username(self):
        """Test that email is used as username."""
        form_data = {
            'email': 'custom@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.username == 'custom@example.com'
    
    def test_form_required_fields(self):
        """Test required fields are enforced."""
        form = CustomUserCreationForm(data={})
        assert not form.is_valid()
        assert 'email' in form.errors
        assert 'password1' in form.errors
        assert 'password2' in form.errors
    
    def test_form_password_validation(self):
        """Test password validation rules."""
        form_data = {
            'email': 'newuser@example.com',
            'password1': 'pass',
            'password2': 'pass'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
