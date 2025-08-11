from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.v1.permissions import IsAdminOrReadOnly
from .serializers import EmployeeSerializer
from services.employee_service import EmployeeService


class EmployeeListCreateAPIView(APIView):
    #permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get(self, request):
        employees = EmployeeService.list_employees()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                employee = EmployeeService.create_employee(
                    name=serializer.validated_data['name'],
                    email=serializer.validated_data['email'],
                    department=serializer.validated_data['department']
                )
                return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeRetrieveUpdateDestroyAPIView(APIView):
    #permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get(self, request, pk):
        employee = EmployeeService.get_employee(pk)
        if not employee:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    def put(self, request, pk):
        employee = EmployeeService.get_employee(pk)
        if not employee:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            try:
                updated_employee = EmployeeService.update_employee(pk, **serializer.validated_data)
                return Response(EmployeeSerializer(updated_employee).data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if EmployeeService.delete_employee(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)