from rest_framework import serializers

from KanMind.boards.models import Board


class BoardSerializer(serializers.ModelSerializer):
    PERMISSION_CLASSES = []

    class Meta:
        model = Board
        fields = '__all__'
