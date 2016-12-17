from rest_framework import viewsets

from .models import Farmer
from .serializers import FarmerSerializer


class FarmerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    filter_fields = ('town',)
