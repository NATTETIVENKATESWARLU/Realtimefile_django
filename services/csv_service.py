import csv
import io
from datetime import datetime
from typing import List, Dict
from django.core.exceptions import ValidationError
from db.models.asset import Asset
from db.models.employee import Employee

class CSVService:
    @staticmethod
    def import_assets_from_csv(csv_file) -> List[Asset]:
        """
        Import assets from CSV file
        Expected format:
        name,asset_type,serial_number,purchase_date,assigned_to,notes
        """
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        assets = []
        errors = []
        
        for row_num, row in enumerate(reader, start=1):
            try:
                # Prepare data
                assigned_to = row.get('assigned_to', '').strip()
                employee = None
                if assigned_to:
                    try:
                        employee = Employee.objects.get(email=assigned_to.lower())
                    except Employee.DoesNotExist:
                        raise ValidationError(f"Employee with email {assigned_to} does not exist")
                
                # Create asset
                asset = Asset(
                    name=row['name'],
                    asset_type=row['asset_type'],
                    serial_number=row.get('serial_number'),
                    purchase_date=datetime.strptime(row['purchase_date'], '%Y-%m-%d').date(),
                    assigned_to=employee,
                    notes=row.get('notes')
                )
                asset.full_clean()
                asset.save()
                assets.append(asset)
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        if errors:
            raise ValidationError("\n".join(errors))
        
        return assets

    @staticmethod
    def export_assets_to_csv() -> str:
        """
        Export assets to CSV format
        """
        assets = Asset.objects.all().select_related('assigned_to')
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'name', 'asset_type', 'serial_number', 
            'purchase_date', 'assigned_to', 'assigned_email', 'notes'
        ])
        
        # Write data
        for asset in assets:
            writer.writerow([
                asset.name,
                asset.asset_type,
                asset.serial_number,
                asset.purchase_date.strftime('%Y-%m-%d'),
                asset.assigned_to.name if asset.assigned_to else '',
                asset.assigned_to.email if asset.assigned_to else '',
                asset.notes or ''
            ])
        
        return output.getvalue()