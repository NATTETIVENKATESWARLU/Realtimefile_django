from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.v1.permissions import IsAdminOrReadOnly
from .serializers import AssetSerializer
from services.asset_service import AssetService
from services.csv_service import CSVService

class AssetListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get(self, request):
        assets = AssetService.list_assets()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                asset = AssetService.create_asset(
                    name=serializer.validated_data['name'],
                    asset_type=serializer.validated_data['asset_type'],
                    serial_number=serializer.validated_data.get('serial_number'),
                    purchase_date=serializer.validated_data['purchase_date'],
                    assigned_to=serializer.validated_data.get('assigned_to'),
                    notes=serializer.validated_data.get('notes')
                )
                return Response(AssetSerializer(asset).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get(self, request, pk):
        asset = AssetService.get_asset(pk)
        if not asset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AssetSerializer(asset)
        return Response(serializer.data)
    
    def put(self, request, pk):
        asset = AssetService.get_asset(pk)
        if not asset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AssetSerializer(asset, data=request.data)
        if serializer.is_valid():
            try:
                updated_asset = AssetService.update_asset(pk, **serializer.validated_data)
                return Response(AssetSerializer(updated_asset).data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if AssetService.delete_asset(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class AssetImportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def post(self, request):
        serializer = AssetImportSerializer(data=request.data)
        if serializer.is_valid():
            try:
                csv_file = serializer.validated_data['csv_file']
                assets = CSVService.import_assets_from_csv(csv_file)
                return Response(
                    AssetSerializer(assets, many=True).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetExportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            csv_data = CSVService.export_assets_to_csv()
            response = Response(csv_data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="assets_export.csv"'
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)