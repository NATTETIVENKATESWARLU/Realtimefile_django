from rest_framework import serializers
from db.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']