from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from goals.filters import GoalFilter, GoalCommentFilter
from goals.models import GoalCategory, Goal, GoalComment
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user.id,
            is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)
        return instance


class GoalCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GoalSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalFilter
    ordering_fields = ['title', 'description']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False)
        )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False)
        )


class CommentCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GoalCommentCreateSerializer


class CommentListView(generics.ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalCommentFilter
    ordering_fields = ('created',)
    ordering = ('-created',)

    def get_queryset(self):
        return GoalComment.objects.prefetch_related('goal').filter(
            Q(user_id=self.request.user.id) & ~Q(goal__status=Goal.Status.archived) & Q(
                goal__category__is_deleted=False)
        )


class CommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.prefetch_related('goal').filter(
            Q(user_id=self.request.user.id) & ~Q(goal__status=Goal.Status.archived) & Q(
                goal__category__is_deleted=False)
        )
