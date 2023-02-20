from rest_framework import permissions

from goals.models import BoardParticipant, Board, GoalCategory, Goal, GoalComment


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id


class BoardPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Board):
        _filters: dict = {
            "user": request.user,
            "board": obj,
        }
        if request.method not in permissions.SAFE_METHODS:
            _filters["role"] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalCategory):
        _filters: dict = {
            "user_id": request.user.id,
            "board_id": obj.board_id,
        }
        if request.method not in permissions.SAFE_METHODS:
            _filters["role__in"] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Goal):
        _filters: dict = {
            "user_id": request.user.id,
            "board_id": obj.category.board_id,
        }
        if request.method not in permissions.SAFE_METHODS:
            _filters["role__in"] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**_filters).exists()


class CommentPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalComment):
        return any((
            request.method in permissions.SAFE_METHODS,
            obj.user.id == request.user.id
        ))
