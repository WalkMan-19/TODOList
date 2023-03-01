from pytest_factoryboy import register

from tests.factories import UserFactory, BoardFactory, BoardParticipantFactory

pytest_plugins = ["tests.fixtures", "tests.factories"]

register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
