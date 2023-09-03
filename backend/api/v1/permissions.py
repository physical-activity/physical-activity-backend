from rest_framework.permissions import IsAuthenticated


class AuthorOnly(IsAuthenticated):
    """Only Author Access."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
