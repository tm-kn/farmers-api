from rest_framework import serializers

from .models import Farmer


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ('id', 'first_name', 'surname', 'town', 'url')
