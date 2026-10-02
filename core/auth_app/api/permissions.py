from django.conf import settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly


def is_guest_user(user):
    guest_email = getattr(settings, 'GUEST_USER_EMAIL', '')
    email = getattr(user, 'email', '')
    return bool(
        guest_email
        and getattr(user, 'is_authenticated', False)
        and email.casefold() == guest_email.casefold()
    )


class GuestAccessPermissionMixin:
    """Allow the configured guest account to bypass permission checks."""

    def has_permission(self, request, view):
        if is_guest_user(request.user):
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if is_guest_user(request.user):
            return True
        return self._has_non_guest_object_permission(request, view, obj)

    def _has_non_guest_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class GuestAwareIsAuthenticatedOrReadOnly(
    GuestAccessPermissionMixin,
    IsAuthenticatedOrReadOnly,
):
    """Apply guest access to default-permission endpoints."""
