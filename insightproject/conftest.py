import os
import django
from django.conf import settings
import pytest

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insightproject.settings')

def pytest_configure():
    """Configure Django settings before running tests."""
    # Force use of SQLite for tests
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    
    if not settings.configured:
        django.setup()
