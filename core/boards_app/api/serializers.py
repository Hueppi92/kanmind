from rest_framework import serializers
from django.contrib.auth.models import User
from core.boards_app.models import Board


class BoardSerializer(serializers.ModelSerializer):
    """Serialize board data while keeping owner and member count read-only."""

    PERMISSION_CLASSES = []
    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'owner', 'title', 'members', 'member_count')
        read_only_fields = ('owner', 'member_count')
