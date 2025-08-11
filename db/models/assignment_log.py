from django.db import models
from .employee import Employee
from .asset import Asset
from django.utils import timezone

class AssetAssignmentLog(models.Model):
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='assignment_logs'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='asset_assignments'
    )
    assigned_on = models.DateTimeField(auto_now_add=True)
    returned_on = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-assigned_on']
        verbose_name = 'Asset Assignment Log'
        verbose_name_plural = 'Asset Assignment Logs'
        get_latest_by = 'assigned_on'

    def __str__(self):
        return f"{self.asset} assigned to {self.employee} on {self.assigned_on}"

    def save(self, *args, **kwargs):
        if not self.pk:  # New assignment
            self.asset.assigned_to = self.employee
            self.asset.save()
        super().save(*args, **kwargs)

    def mark_returned(self):
        if not self.returned_on:
            self.returned_on = timezone.now()
            self.asset.assigned_to = None
            self.asset.save()
            self.save()