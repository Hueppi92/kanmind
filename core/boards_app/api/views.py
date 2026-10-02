from django.db.models import Count, Q

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response

from core.boards_app.models import Board
from core.boards_app.api.serializers import BoardListSerializer, BoardSerializer
from core.boards_app.api.permissions import IsMemberOrOwner, IsOwner
from core.auth_app.api.permissions import is_guest_user


def _boards_with_member_count():
    """Annotate boards with member and task summary counts."""
    return Board.objects.annotate(
        member_count=Count('members', distinct=True),
        ticket_count=Count('task', distinct=True),
        tasks_to_do_count=Count(
            'task',
            filter=Q(task__status='to-do'),
            distinct=True,
        ),
        tasks_high_prio_count=Count(
            'task',
            filter=Q(task__priority='high'),
            distinct=True,
        ),
    )


class BoardViewSet(viewsets.ModelViewSet):
    """Provide board CRUD while limiting access to owners and members."""

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return BoardListSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsOwner]
        elif self.action in ('retrieve', 'update', 'partial_update'):
            permission_classes = [IsMemberOrOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        boards = _boards_with_member_count()
        if self.action != 'list' or is_guest_user(self.request.user):
            return boards
        return boards.filter(
            Q(members=self.request.user)
            | Q(owner=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
