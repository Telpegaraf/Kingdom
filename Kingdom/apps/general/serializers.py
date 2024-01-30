from rest_framework import serializers
from apps.general.models import FeatTrait


class FeatTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatTrait
        fields = ['id', 'name', 'description']
