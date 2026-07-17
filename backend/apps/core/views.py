from rest_framework import viewsets
from .models import Province, City
from .serializers import ProvinceSerializer, CitySerializer

class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    pagination_class = None

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    pagination_class = None

    def get_queryset(self):
        queryset = City.objects.all()
        province_id = self.request.query_params.get('province_id', None)
        if province_id is not None:
            queryset = queryset.filter(province_id=province_id)
        return queryset
