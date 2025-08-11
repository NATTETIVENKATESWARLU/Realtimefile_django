from rest_framework import serializers
from db.models import AssetAssignmentLog

class AssetAssignmentSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_email = serializers.CharField(source='employee.email', read_only=True)
    
    class Meta:
        model = AssetAssignmentLog
        fields = [
            'id', 'asset', 'asset_name', 'employee', 'employee_name', 'employee_email',
            'assigned_on', 'returned_on', 'notes'
        ]
        read_only_fields = ['id', 'assigned_on', 'returned_on']

class AssetImportSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def validate_csv_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed")
        return value