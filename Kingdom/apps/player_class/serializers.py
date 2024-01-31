from rest_framework import serializers
from apps.player_class.models import ClassFeature, ClassFeat, ClassSpellFeature
from apps.general.serializers import FeatTraitSerializer


class FeatsSerializer(serializers.ModelSerializer):
    class_character = serializers.StringRelatedField()
    action = serializers.StringRelatedField()
    prerequisite = serializers.StringRelatedField()
    requirements = serializers.StringRelatedField()
    traits = FeatTraitSerializer(many=True)
    trigger = serializers.StringRelatedField()

    class Meta:
        model = ClassFeat
        fields = ['id', 'name', 'description', 'trigger', 'class_character', 'level', 'action', 'prerequisite',
                  'traits', 'requirements']


class FeatureListSerializer(serializers.ModelSerializer):
    class_player = serializers.StringRelatedField()
    feats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = ClassFeature
        fields = ['id', 'class_player', 'level', 'feats', 'class_feat_count', 'general_feat_count',
                  'background_feat_count', 'skill_count', 'stats_boost']


class SpellFeatureListSerializer(serializers.ModelSerializer):
    class_player = serializers.StringRelatedField()

    class Meta:
        model = ClassSpellFeature
        fields = '__all__'
