from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated', 'user', 'is_deleted']


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated', 'user', 'is_deleted']


class GoalCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated', 'user']

    def validate_category(self, value):
        if self.context['request'].user != value.user:
            raise exceptions.PermissionDenied
        return value


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated', 'user']


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ['created', 'updated']

    def validate_goal(self, goal: Goal):
        if goal.category.is_deleted:
            raise ValidationError('Cannot create a comment for a category in the archive')
        if self.context['request'].user != goal.user:
            raise exceptions.PermissionDenied
        return goal


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ['created', 'updated']
