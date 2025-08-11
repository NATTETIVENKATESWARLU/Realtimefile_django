from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class Department(models.TextChoices):
    IT = 'IT', 'Information Technology'
    HR = 'HR', 'Human Resources'
    FINANCE = 'FIN', 'Finance'
    MARKETING = 'MKT', 'Marketing'
    OPERATIONS = 'OPS', 'Operations'

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    department = models.CharField(
        max_length=3,
        choices=Department.choices,
        default=Department.IT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.name} ({self.email})"

    def clean(self):
        super().clean()
        if not self.email:
            raise ValidationError({'email': 'Email is required.'})
        self.email = self.email.lower()