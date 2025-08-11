from django.db import models
from django.core.exceptions import ValidationError
from .employee import Employee

class AssetType(models.TextChoices):
    HARDWARE = 'HW', 'Hardware'
    SOFTWARE = 'SW', 'Software'

class Asset(models.Model):
    name = models.CharField(max_length=100)
    asset_type = models.CharField(
        max_length=2,
        choices=AssetType.choices,
        default=AssetType.HARDWARE
    )
    serial_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    purchase_date = models.DateField()
    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-purchase_date']
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        constraints = [models.UniqueConstraint(
                fields=['serial_number'],
                name='unique_serial_number',
                condition=models.Q(serial_number__isnull=False)
        )]

    def __str__(self):
        return f"{self.get_asset_type_display()}: {self.name} ({self.serial_number})"

    def clean(self):
        super().clean()
        if self.asset_type == AssetType.HARDWARE and not self.serial_number:
            raise ValidationError({'serial_number': 'Hardware assets must have a serial number.'})