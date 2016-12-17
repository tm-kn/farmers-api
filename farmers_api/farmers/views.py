from rest_framework import viewsets, permissions

from .models import Farmer
from .serializers import FarmerSerializer


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    filter_fields = ('town',)
    permissions = permissions.DjangoModelPermissionsOrAnonReadOnly
