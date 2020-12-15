from uuid import uuid4

from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Manager for User Model
        Defines create_user and create_superuser functions to use email as username
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Model for User Accounts
    Extends Django's AbstractUser Class, which provides the following fields
        * username
            * Set to None so it is not used
        * first_name
            * Overwritten to invalidate empty string
        * last_name
            * Overwritten to invalidate empty string
        * email
            * Overwritten to require unique emails and use as the username field
        * is_staff
        * is_active
        * date_joined
        * password
        * last_login
        * is_superuser
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)
    username = None
    is_vendor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'is_vendor']

    objects = UserManager()


class Printer(models.Model):
    """
    Model for Printers belonging to Vendors
    """

    DIMENSION_CHOICES = [
        ('in', 'inches'),
        ('cm', 'centimeters'),
        ('mm', 'millimeters')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    dimension_unit = models.CharField(choices=DIMENSION_CHOICES, max_length=2)
    filaments = models.CharField(max_length=1000)
    make = models.CharField(max_length=100)
    max_print_dimension_x = models.IntegerField(
        validators=[MinValueValidator(0)])
    max_print_dimension_y = models.IntegerField(
        validators=[MinValueValidator(0)])
    max_print_dimension_z = models.IntegerField(
        validators=[MinValueValidator(0)])
    model = models.CharField(max_length=150)
    vendor = models.OneToOneField(User, on_delete=models.PROTECT)
