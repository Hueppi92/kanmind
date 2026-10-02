from rest_framework import serializers
from django.contrib.auth.models import User
from core.boards_app.models import Board
from ..models import Task, Comment


class TaskUserSerializer(serializers.ModelSerializer):
    """Expose the public user details nested in task responses."""

    class Meta:
        model = User
        fields = ('id', 'fullname', 'email')

    fullname = serializers.CharField(source='get_full_name', read_only=True)


class TaskSerializer(serializers.ModelSerializer):
    """Serialize task fields and nested assignee/reviewer details."""

    class Meta:
        model = Task
        fields = (
            'id', 'board', 'title', 'description', 'status', 'priority',
            'due_date', 'assignee', 'assignee_id', 'reviewer', 'reviewer_id',
            'comments_count',
        )
    comments_count = serializers.IntegerField(read_only=True)
    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(), required=True)
    assignee = TaskUserSerializer(read_only=True)
    reviewer = TaskUserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee',
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer',
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )

    def validate_assignee(self, attrs):
        board = attrs.get(
            'board', self.instance.board if self.instance else None)
        if (
            self.instance
            and 'board' in attrs
            and board.pk != self.instance.board_id
        ):
            raise serializers.ValidationError(
                {'board': 'Changing the task board is not allowed.'}
            )

        if 'assignee' in attrs:
            if (
                attrs['assignee'] is not None
                and not board.members.filter(
                    pk=attrs['assignee'].pk
                ).exists()
            ):
                raise serializers.ValidationError(
                    "Assignee must be a member of the board.")
        return attrs

    def validate_reviewer(self, attrs):
        board = attrs.get(
            'board', self.instance.board if self.instance else None)
        if (
            self.instance
            and 'board' in attrs
            and board.pk != self.instance.board_id
        ):
            raise serializers.ValidationError(
                {'board': 'Changing the task board is not allowed.'}
            )

        if 'reviewer' in attrs:
            if (
                attrs['reviewer'] is not None
                and not board.members.filter(
                    pk=attrs['reviewer'].pk
                ).exists()
            ):
                raise serializers.ValidationError(
                    "Reviewer must be a member of the board.")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Serialize comment data without allowing clients to set its author."""

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'author', 'content')

    author = serializers.CharField(
        source='author.get_full_name', read_only=True)
