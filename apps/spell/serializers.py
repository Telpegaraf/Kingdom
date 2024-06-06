from rest_framework import serializers
from apps.spell.models import Spell, SpellCast, SpellComponent, SpellTrait, SpellSchool, SpellTradition


class SpellSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellSchool
        fields = ['name', 'description']


class SpellTraditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellTradition
        fields = ['name', 'description']


class SpellCastSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellCast
        fields = '__all__'


class SpellComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellComponent
        fields = ['name', 'description']


class SpellTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellTrait
        fields = ['name', 'description']


class SpellListSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()

    class Meta:
        model = Spell
        fields = ['name', 'school', 'level']


class SpellDetailSerializer(serializers.ModelSerializer):
    school = SpellSchoolSerializer()
    tradition = SpellTraditionSerializer(many=True)
    trait = SpellTraitSerializer(many=True)
    component = SpellComponentSerializer(many=True)
    primary_check = serializers.StringRelatedField(many=True)
    secondary_check = serializers.StringRelatedField(many=True)

    class Meta:
        model = Spell
        fields = ['name', 'description', 'level', 'school', 'tradition', 'trait', 'component', 'cast', 'spell_range',
                  'duration', 'sustain', 'ritual', 'secondary_casters', 'cost', 'primary_check', 'secondary_check',
                  'target', 'source']
