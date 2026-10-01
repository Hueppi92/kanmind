from rest_framework.permissions import IsAuthenticated

from core.boards_app.models import Board
from core.tasks_app.models import Comment, Task


def _get_board(obj):
    if hasattr(obj, "members") and hasattr(obj, "owner"):
        return obj
    if hasattr(obj, "board"):
        return obj.board
    task = getattr(obj, "task", None)
    if task is not None:
        return task.board
    return None


class IsMemberOrOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        board = _get_board(obj)
        if board is None:
            return False
        return (
            board.owner_id == request.user.pk
            or board.members.filter(pk=request.user.pk).exists()
        )


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        board = _get_board(obj)
        return board is not None and board.owner_id == request.user.pk


class IsMember(IsAuthenticated):
    def has_permission(self, request, view):
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

    def has_object_permission(self, request, view, obj):
        board = _get_board(obj)
        if board is None or not board.members.filter(pk=request.user.pk).exists():
            return False
        if request.method in ("PUT", "PATCH") and "board" in request.data:
            return str(request.data["board"]) == str(obj.board_id)
        return True


class IsMemberOfTask(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        task_id = getattr(view, "kwargs", {}).get("pk")
        if task_id is None:
            return True
        task = Task.objects.filter(pk=task_id).select_related("board").first()
        if task is None:
            return True
        return task.board.members.filter(pk=request.user.pk).exists()


class IsTaskCreatorOrBoardOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            getattr(obj, "creator_id", None) == request.user.pk
            or getattr(getattr(obj, "board", None), "owner_id", None)
            == request.user.pk
        )


class IsCreatorOfComment(IsAuthenticated):
    def has_permission(self, request, view):
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

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "author_id", None) == request.user.pk

