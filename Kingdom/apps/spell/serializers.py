from rest_framework import serializers
from apps.spell.models import Spell, SpellCast, SpellComponent, SpellTrait, SpellSchool, SpellTradition


class SpellSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellSchool
        fields = '__all__'


class SpellTraditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellTradition
        fields = '__all__'


class SpellCastSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellCast
        fields = '__all__'


class SpellComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellComponent
        fields = '__all__'


class SpellTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellTrait
        fields = '__all__'


class SpellOverallSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    tradition = serializers.StringRelatedField(many=True)
    trait = serializers.StringRelatedField(many=True)
    component = serializers.StringRelatedField(many=True)
    primary_check = serializers.StringRelatedField(many=True)
    secondary_check = serializers.StringRelatedField(many=True)

    class Meta:
        model = Spell
        fields = ['name', 'description', 'level', 'school', 'tradition', 'trait', 'component', 'cast', 'spell_range',
                  'duration', 'sustain', 'ritual', 'secondary_casters', 'cost', 'primary_check', 'secondary_check',
                  'target', 'source']
