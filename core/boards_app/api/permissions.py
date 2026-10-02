from rest_framework.permissions import IsAuthenticated


def _get_board(obj):
	"""Resolve a board from a board, task, or comment instance."""
	if hasattr(obj, "members") and hasattr(obj, "owner"):
		return obj
	if hasattr(obj, "board"):
		return obj.board
	task = getattr(obj, "task", None)
	if task is not None:
		return task.board
	return None


class IsMemberOrOwner(IsAuthenticated):
	"""Allow access when the user owns or belongs to the object's board."""

	def has_object_permission(self, request, view, obj):
		board = _get_board(obj)
		if board is None:
			return False
		return (
			board.owner_id == request.user.pk
			or board.members.filter(pk=request.user.pk).exists()
		)


class IsOwner(IsAuthenticated):
	"""Restrict board-level actions to the board owner."""

	def has_object_permission(self, request, view, obj):
		board = _get_board(obj)
		return board is not None and board.owner_id == request.user.pk
