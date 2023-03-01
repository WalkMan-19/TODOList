import factory
from django.contrib.auth.hashers import make_password
from factory import post_generation, fuzzy

from core.models import User
from goals.models import Board, BoardParticipant


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs['password'] = make_password(kwargs['password'])
        return super(UserFactory, cls)._create(model_class, *args, **kwargs)


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker('text')

    @post_generation
    def owner(self, create, owner):
        if not create:
            return
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    role = fuzzy.FuzzyChoice(BoardParticipant.Role.choices[1:], getter=lambda role: role[0])
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
