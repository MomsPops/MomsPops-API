from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .fields import Base64ImageField
from .models import Reaction, ReactionItem


class ReactionItemSerializer(ModelSerializer):
    image = Base64ImageField(max_length=None)

    class Meta:
        model = ReactionItem
        fields = ('id', 'image')


class ReactionSerializer(ModelSerializer):
    reaction_option = ReactionItemSerializer()
    owner = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Reaction
        fields = ('id', 'reaction_option', 'owner')
