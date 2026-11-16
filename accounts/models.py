from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    ADMIN, MEMBER = 'admin', 'member'
    ROLE_CHOICES = [(ADMIN, 'Admin'), (MEMBER, 'Member')]

    LENDER, BORROWER, BOTH = 'lender', 'borrower', 'both'
    ACCOUNT_TYPE_CHOICES = [
        (LENDER, 'Lender'),
        (BORROWER, 'Borrower'),
        (BOTH, 'Both lender and borrower'),
    ]

    username = None
    email = models.EmailField('email address', unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MEMBER)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default=BOTH)
    contact_number = models.CharField(max_length=20, blank=True)
    barangay = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def can_lend(self):
        return self.account_type in (self.LENDER, self.BOTH)

    @property
    def can_borrow(self):
        return self.account_type in (self.BORROWER, self.BOTH)