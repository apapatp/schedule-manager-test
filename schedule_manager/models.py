from django.db import models
from django.utils import timezone
from abstract.models import AbstractModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    """Custom user manager class."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError("User must have an email address")
        elif not password:
            raise ValueError("User must have a password")

        # Normalize the email address
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        if not email:
            raise ValueError("Superuser must have an email address")
        elif not password:
            raise ValueError("Superuser must have a password")

        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, AbstractModel, PermissionsMixin):
    """
    Override the default user model.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    last_logout_at = models.DateTimeField(blank=True, null=True)

    # User Manager
    objects = UserManager()

    # Default field for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def update_last_logout_at(self):
        """Update the last logout time."""
        self.last_logout_at = timezone.now()
        self.save(update_fields=["last_logout_at"])

    @property
    def is_staff(self):
        """Return boolean value for superuser status."""
        return self.is_superuser

    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else None

    def __str__(self):
        """Return the string representation of the user."""
        return self.email


class Schedule(AbstractModel):
    """
    Schedule model.
    """

    class DaysChoices(models.TextChoices):
        """Choices for the days of the week."""
        MONDAY = "monday", "Monday"
        TUESDAY = "tuesday", "Tuesday"
        WEDNESDAY = "wednesday", "Wednesday"
        THURSDAY = "thursday", "Thursday"
        FRIDAY = "friday", "Friday"
        SATURDAY = "saturday", "Saturday"
        SUNDAY = "sunday", "Sunday"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")
    day = models.CharField(max_length=10, choices=DaysChoices.choices)
    camera_ids = models.JSONField(default=list, blank=True, null=True)
    badge_ids = models.JSONField(default=list, blank=True, null=True)
    start = models.TimeField()
    stop = models.TimeField()

    def __str__(self):
        """Return the string representation of the schedule."""
        return f"{self.user.email} - {self.day} - {self.start} - {self.stop}"
