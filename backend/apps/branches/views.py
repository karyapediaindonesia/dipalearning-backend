from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from .models import Branch
from .serializers import BranchSerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.filter(is_active=True)
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]

from .models import Room
from .serializers import RoomSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('code')
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.delete()


from .models import Holiday
from .serializers import HolidaySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from datetime import datetime

class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['post'])
    def sync_national_holidays(self, request):
        year = request.data.get('year', datetime.now().year)
        branch_id = request.data.get('branch_id')
        
        if not branch_id:
            return Response({'detail': 'ID Cabang wajib dipilih.'}, status=400)
            
        current_year = datetime.now().year
        years_to_sync = [current_year, current_year + 1, current_year + 2]
        holidays_data = []
        
        for y in years_to_sync:
            try:
                # Menggunakan nager API sebagai fallback multi-tahun yang aman
                api_url = f'https://date.nager.at/api/v3/PublicHolidays/{y}/ID'
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for item in data:
                        holidays_data.append({
                            'date': item.get('date'),
                            'name': item.get('localName') or item.get('name')
                        })
            except requests.exceptions.RequestException:
                pass
                
        if not holidays_data:
             return Response({'detail': 'Gagal mengambil data kalender.'}, status=502)
            
        synced_count = 0
        
        # If 'ALL' is passed (handled by frontend if all branches selected), we can handle it.
        # But to keep it simple, frontend will send the specific branch ID, or we can handle 'all' here.
        if branch_id == 'all':
            branches = Branch.objects.filter(is_active=True)
        else:
            try:
                branches = [Branch.objects.get(id=branch_id)]
            except Branch.DoesNotExist:
                return Response({'detail': 'Cabang tidak ditemukan.'}, status=404)
        
        for branch in branches:
            for item in holidays_data:
                date_str = item.get('date')
                name = item.get('name')
                
                if date_str and name:
                    Holiday.objects.update_or_create(
                        branch=branch,
                        date_start=date_str,
                        defaults={
                            'name': name,
                            'date_end': date_str,
                            'holiday_type': 'NATIONAL',
                            'operational_impact': 'FULL_CLOSE',
                            'status': 'ACTIVE',
                            'notes': 'Diambil otomatis dari API Sinkronisasi.'
                        }
                    )
            synced_count += len(holidays_data)
                
        return Response({'detail': f'Berhasil mensinkronisasi {len(holidays_data)} hari libur ke {len(branches)} cabang.'})
