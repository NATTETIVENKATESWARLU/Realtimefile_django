from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import AssetAssignmentSerializer
from services.asset_service import AssetService

class AssetAssignmentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AssetAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                assignment = AssetService.assign_asset(
                    asset_id=serializer.validated_data['asset'].id,
                    employee_id=serializer.validated_data['employee'].id,
                    notes=serializer.validated_data.get('notes')
                )
                return Response(
                    AssetAssignmentSerializer(assignment).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetReturnAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, asset_id):
        try:
            assignment = AssetService.return_asset(asset_id)
            return Response(AssetAssignmentSerializer(assignment).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)