from rest_framework import serializers

from KanMind.boards.models import Board


class BoardSerializer(serializers.ModelSerializer):
    PERMISSION_CLASSES = []
    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'owner', 'title', 'members', 'member_count')
        read_only_fields = ('owner', 'member_count')

