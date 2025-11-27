import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating test User objects."""
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'testuser{n}')
    email = factory.Sequence(lambda n: f'testuser{n}@example.com')
    password = 'testpass123!'
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    
    @classmethod
    def create(cls, **kwargs):
        """Override create to hash password properly."""
        obj = super().create(**kwargs)
        if 'password' in kwargs:
            obj.set_password(kwargs['password'])
            obj.save()
        return obj
