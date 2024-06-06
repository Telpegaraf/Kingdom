from rest_framework import serializers
from .models import Kingdom, Region, City


class CitySerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()
    form_of_government = serializers.StringRelatedField()
    ruler = serializers.StringRelatedField()
    temples = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'region', 'form_of_government', 'ruler', 'population', 'temples', 'blazon']


class RegionSerializer(serializers.ModelSerializer):
    cities = CitySerializer(
        many=True,
        read_only=True,
        source='city',
    )
    kingdom = serializers.StringRelatedField()
    form_of_government = serializers.StringRelatedField()
    ruler = serializers.StringRelatedField()

    class Meta:
        model = Region
        fields = ['id', 'name', 'kingdom', 'form_of_government', 'ruler', 'population', 'cities']


class CityOverallSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(
        many=True,
        read_only=True,
        source='region',
    )
    form_of_government = serializers.StringRelatedField()
    ruler = serializers.StringRelatedField()

    class Meta:
        model = Kingdom
        fields = ['id', 'name', 'form_of_government', 'ruler', 'population', 'regions']
