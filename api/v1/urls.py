from django.urls import path
from api.v1.employees.views import (
    EmployeeListCreateAPIView,
    EmployeeRetrieveUpdateDestroyAPIView
)
from api.v1.assets.views import (
    AssetListCreateAPIView,
    AssetRetrieveUpdateDestroyAPIView,
    AssetImportAPIView,
    AssetExportAPIView
)
from api.v1.assignments.views import (
    AssetAssignmentAPIView,
    AssetReturnAPIView
)

urlpatterns = [
    # Employees
    path('employees/', EmployeeListCreateAPIView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyAPIView.as_view(), name='employee-detail'),
    
    # Assets
    path('assets/', AssetListCreateAPIView.as_view(), name='asset-list'),
    path('assets/<int:pk>/', AssetRetrieveUpdateDestroyAPIView.as_view(), name='asset-detail'),
    path('assets/import/', AssetImportAPIView.as_view(), name='asset-import'),
    path('assets/export/', AssetExportAPIView.as_view(), name='asset-export'),
    
    # Assignments
    path('assignments/', AssetAssignmentAPIView.as_view(), name='asset-assignment'),
    path('assets/<int:asset_id>/return/', AssetReturnAPIView.as_view(), name='asset-return'),
]