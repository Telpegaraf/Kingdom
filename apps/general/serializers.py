from rest_framework import serializers
from apps.general.apps import FeatTrait, Skills, WeaponMastery


class FeatTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatTrait
        fields = ['id', 'name', 'description']


class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id', 'name', 'description']


class WeaponMasteryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponMastery
        fields = ['id', 'name', 'description']
