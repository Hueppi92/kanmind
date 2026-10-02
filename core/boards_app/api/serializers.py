from rest_framework import serializers
from core.boards_app.models import Board


class BoardSerializer(serializers.ModelSerializer):
    """Serialize board data while keeping owner and member count read-only."""

    PERMISSION_CLASSES = []
    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'owner', 'title', 'members', 'member_count')
        read_only_fields = ('owner', 'member_count')


class BoardListSerializer(serializers.ModelSerializer):
    """Serialize the summary fields returned by the board list endpoint."""

    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = (
            'id',
            'title',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id',
        )
