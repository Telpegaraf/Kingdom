from rest_framework import serializers
from .models import God, Domains


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domains
        fields = '__all__'


class GodOverallSerializer(serializers.ModelSerializer):
    domain = DomainSerializer(read_only=True, many=True)

    class Meta:
        model = God
        fields = '__all__'
