from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from social_media_assignment.base_models import BaseModel


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, BaseModel):
    """
    A custom user class implementing a fully featured User model with
    admin-compliant permissions.

    Username, Email and password are required. Other fields are optional.
    """
    email = models.EmailField(
        'email address',
        max_length=255,
        unique=True
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )

    is_active = models.BooleanField('active',
                                    default=True,
                                    help_text='Designates whether this user should be treated as active. '
                                              'Unselect this instead of deleting accounts.'
                                    )
    is_staff = models.BooleanField('staff status',
                                   default=False,
                                   help_text='Designates whether the user can log into this admin site.',
                                   )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    # groups = None

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        """
        to set table name in database
        """
        verbose_name = 'user'
        verbose_name_plural = 'users'


class UserProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    followers = models.ManyToManyField(CustomUser, related_name='following', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


