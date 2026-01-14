from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _



class Faculty(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=32, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, related_name="students")

    def __str__(self) -> str:
        return f"{self.student_id} ({self.user.username})"


class WasteEntry(models.Model):
    CATEGORY_CHOICES = [
        ("plastic", _("Plastic")),
        ("paper", _("Paper")),
        ("glass", _("Glass")),
        ("metal", _("Metal")),
        ("organic", _("Organic")),
        ("electronic", _("Electronic")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="waste_entries",
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2)  # 0.01..999.99
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.category} {self.weight_kg} kg"
