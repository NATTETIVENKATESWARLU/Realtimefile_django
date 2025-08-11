from typing import Optional, List, Dict
from django.core.exceptions import ValidationError
from db.models.employee import Employee

class EmployeeService:
    @staticmethod
    def create_employee(name: str, email: str, department: str) -> Employee:
        """
        Create a new employee with validation
        """
        employee = Employee(name=name, email=email, department=department)
        employee.full_clean()
        employee.save()
        return employee

    @staticmethod
    def update_employee(employee_id: int, **kwargs) -> Employee:
        """
        Update employee details
        """
        employee = Employee.objects.get(pk=employee_id)
        for field, value in kwargs.items():
            setattr(employee, field, value)
        employee.full_clean()
        employee.save()
        return employee

    @staticmethod
    def get_employee(employee_id: int) -> Optional[Employee]:
        """
        Get employee by ID
        """
        try:
            return Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            return None

    @staticmethod
    def list_employees(filters: Dict = None) -> List[Employee]:
        """
        List employees with optional filtering
        """
        queryset = Employee.objects.all()
        if filters:
            queryset = queryset.filter(**filters)
        return list(queryset)

    @staticmethod
    def delete_employee(employee_id: int) -> bool:
        """
        Delete an employee
        Returns True if deleted, False if not found
        """
        try:
            employee = Employee.objects.get(pk=employee_id)
            employee.delete()
            return True
        except Employee.DoesNotExist:
            return False