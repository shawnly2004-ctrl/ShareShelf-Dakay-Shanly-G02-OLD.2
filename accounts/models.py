from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN, MEMBER = 'admin', 'member'
    ROLE_CHOICES = [(ADMIN, 'Admin'), (MEMBER, 'Member')]

    LENDER, BORROWER, BOTH = 'lender', 'borrower', 'both'
    ACCOUNT_TYPE_CHOICES = [
        (LENDER, 'Lender'),
        (BORROWER, 'Borrower'),
        (BOTH, 'Both lender and borrower'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MEMBER)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default=BOTH)
    contact_number = models.CharField(max_length=20, blank=True)
    barangay = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ADMIN
        super().save(*args, **kwargs)

    @property
    def can_lend(self):
        return self.account_type in (self.LENDER, self.BOTH)

    @property
    def can_borrow(self):
        return self.account_type in (self.BORROWER, self.BOTH)
