from typing import Optional, List, Dict
from django.core.exceptions import ValidationError
from db.models.asset import Asset
from db.models.employee import Employee
from db.models.assignment_log import AssetAssignmentLog
from datetime import date

class AssetService:
    @staticmethod
    def create_asset(
        name: str,
        asset_type: str,
        purchase_date: date,
        serial_number: str = None,
        assigned_to: int = None,
        notes: str = None
    ) -> Asset:
        """
        Create a new asset with validation
        """
        asset = Asset(
            name=name,
            asset_type=asset_type,
            serial_number=serial_number,
            purchase_date=purchase_date,
            notes=notes
        )
        
        if assigned_to:
            employee = Employee.objects.get(pk=assigned_to)
            asset.assigned_to = employee
        
        asset.full_clean()
        asset.save()
        return asset

    @staticmethod
    def update_asset(asset_id: int, **kwargs) -> Asset:
        """
        Update asset details
        """
        asset = Asset.objects.get(pk=asset_id)
        for field, value in kwargs.items():
            setattr(asset, field, value)
        asset.full_clean()
        asset.save()
        return asset

    @staticmethod
    def get_asset(asset_id: int) -> Optional[Asset]:
        """
        Get asset by ID
        """
        try:
            return Asset.objects.get(pk=asset_id)
        except Asset.DoesNotExist:
            return None

    @staticmethod
    def list_assets(filters: Dict = None) -> List[Asset]:
        """
        List assets with optional filtering
        """
        queryset = Asset.objects.all()
        if filters:
            queryset = queryset.filter(**filters)
        return list(queryset)

    @staticmethod
    def delete_asset(asset_id: int) -> bool:
        """
        Delete an asset
        Returns True if deleted, False if not found
        """
        try:
            asset = Asset.objects.get(pk=asset_id)
            asset.delete()
            return True
        except Asset.DoesNotExist:
            return False

    @staticmethod
    def assign_asset(asset_id: int, employee_id: int, notes: str = None) -> AssetAssignmentLog:
        """
        Assign an asset to an employee
        """
        asset = Asset.objects.get(pk=asset_id)
        employee = Employee.objects.get(pk=employee_id)
        
        if asset.assigned_to == employee:
            raise ValidationError("Asset is already assigned to this employee")
        
        assignment = AssetAssignmentLog(
            asset=asset,
            employee=employee,
            notes=notes
        )
        assignment.save()
        return assignment

    @staticmethod
    def return_asset(asset_id: int) -> AssetAssignmentLog:
        """
        Mark an asset as returned
        """
        asset = Asset.objects.get(pk=asset_id)
        if not asset.assigned_to:
            raise ValidationError("Asset is not currently assigned")
        
        assignment = AssetAssignmentLog.objects.filter(
            asset=asset,
            returned_on__isnull=True
        ).latest('assigned_on')
        
        assignment.mark_returned()
        return assignment