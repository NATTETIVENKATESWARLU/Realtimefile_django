from rest_framework import serializers
from db.models import Asset

class AssetSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.name', read_only=True)
    
    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'asset_type', 'serial_number', 'purchase_date',
            'assigned_to', 'assigned_to_email', 'assigned_to_name', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']