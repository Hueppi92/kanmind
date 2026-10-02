from rest_framework.permissions import IsAuthenticated

from core.auth_app.api.permissions import (
    GuestAccessPermissionMixin,
    is_guest_user,
)
from core.boards_app.models import Board
from core.tasks_app.models import Comment, Task


class IsMember(GuestAccessPermissionMixin, IsAuthenticated):
    """Require membership to create or modify tasks on a board."""

    def has_permission(self, request, view):
        if is_guest_user(request.user):
            return True
        if not super().has_permission(request, view):
            return False
        if getattr(view, "action", None) != "create":
            return True

        board_id = request.data.get("board")
        if board_id is None:
            return False
        try:
            return Board.objects.filter(
                pk=board_id,
                members=request.user,
            ).exists()
        except (TypeError, ValueError):
            return False

    def _has_non_guest_object_permission(self, request, view, obj):
        board = getattr(obj, "board", None)
        if (
            board is None
            or not board.members.filter(pk=request.user.pk).exists()
        ):
            return False
        if request.method in ("PUT", "PATCH") and "board" in request.data:
            return str(request.data["board"]) == str(obj.board_id)
        return True


class IsMemberOfTask(GuestAccessPermissionMixin, IsAuthenticated):
    """Require membership in the task's board for comment operations."""

    def has_permission(self, request, view):
        if is_guest_user(request.user):
            return True
        if not super().has_permission(request, view):
            return False
        task_id = getattr(view, "kwargs", {}).get("pk")
        if task_id is None:
            return True
        task = Task.objects.filter(pk=task_id).select_related("board").first()
        if task is None:
            return True
        return task.board.members.filter(pk=request.user.pk).exists()


class IsTaskCreatorOrBoardOwner(GuestAccessPermissionMixin, IsAuthenticated):
    """Allow task deletion only to its creator or the board owner."""

    def _has_non_guest_object_permission(self, request, view, obj):
        return (
            getattr(obj, "creator_id", None) == request.user.pk
            or getattr(getattr(obj, "board", None), "owner_id", None)
            == request.user.pk
        )


class IsCreatorOfComment(GuestAccessPermissionMixin, IsAuthenticated):
    """Restrict comment deletion to the comment author."""

    def has_permission(self, request, view):
        if is_guest_user(request.user):
            return True
        if not super().has_permission(request, view):
            return False
        comment_id = getattr(view, "kwargs", {}).get("comment_id")
        task_id = getattr(view, "kwargs", {}).get("pk")
        if comment_id is None or task_id is None:
            return True
        comment = Comment.objects.filter(
            pk=comment_id,
            task_id=task_id,
        ).only("author_id").first()
        return comment is None or comment.author_id == request.user.pk

    def _has_non_guest_object_permission(self, request, view, obj):
        return getattr(obj, "author_id", None) == request.user.pk
