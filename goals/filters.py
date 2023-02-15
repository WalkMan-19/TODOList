import django_filters
from django.db import models
from django_filters.rest_framework import FilterSet

from goals.models import Goal, GoalComment


class GoalFilter(FilterSet):
    class Meta:
        model = Goal
        fields = {
            "category": ("exact", "in"),
            "priority": ("exact", "in"),
            "due_date": ("lte", "gte"),
        }

        filter_overrides = {
            models.DateField: {"filter_class": django_filters.IsoDateTimeFilter},
        }


class GoalCommentFilter(FilterSet):
    class Meta:
        model = GoalComment
        fields = {
            'goal': ('exact',)
        }
