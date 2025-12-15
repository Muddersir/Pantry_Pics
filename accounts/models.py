import json
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        # Ensure default values are set on extra_fields to avoid passing duplicate kwargs
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Set defaults for superuser; these will only be used if not provided
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # becomes True after email verification
    is_seller = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# --- JSONTextField fallback for DBs without native JSON support (e.g. SQLite) ---
class JSONTextField(models.TextField):
    description = "JSON encoded data stored in a TextField"

    def from_db_value(self, value, expression, connection):
        if value is None or value == "":
            return {}
        try:
            return json.loads(value)
        except Exception:
            return {}

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None or value == "":
            return {}
        try:
            return json.loads(value)
        except Exception:
            return {}

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            # assume already serialized
            return value
        try:
            return json.dumps(value)
        except Exception:
            return json.dumps({})

# Use native JSONField when available (Postgres or modern Django), otherwise fallback
try:
    JSONFieldSupported = hasattr(models, "JSONField")
except Exception:
    JSONFieldSupported = False

PREFERENCES_FIELD = models.JSONField(default=dict, blank=True) if JSONFieldSupported else JSONTextField(default=dict, blank=True)


class Profile(models.Model):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    preferences = PREFERENCES_FIELD
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Profile: {self.user.email}"
