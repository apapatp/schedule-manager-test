import factory
from schedule_manager.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")

    @classmethod
    def create_superuser(cls, **kwargs):
        """Return created superuser instance."""
        return cls(is_superuser=True, **kwargs)
