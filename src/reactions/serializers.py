from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from reactions.fields import Base64ImageField
from reactions.models import ReactionLike, ReactionItem


class ReactionItemSerializer(ModelSerializer):
    image = Base64ImageField(max_length=None)

    class Meta:
        model = ReactionItem
        fields = ('id', 'image')


class ReactionSerializer(ModelSerializer):
    reaction_option = ReactionItemSerializer()
    owner = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = ReactionLike
        fields = ('id', 'reaction_option', 'owner')


class FanSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source="content_type.name")
    content_object = serializers.CharField(source="content_object.id")

    class Meta:
        model = ReactionLike
        fields = (
            'id',
            'owner ',
            'content_type',
            'content_object',
            'ReactionItem'
        )
