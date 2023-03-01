import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User
from goals.models import BoardParticipant, Board
from goals.serializers import BoardSerializer


@pytest.mark.django_db
class TestBoardCreate:
    url = reverse('create-board')

    def test_board_create_success(self, login_user, current_user, faker):
        title = faker.text(max_nb_chars=255)

        response = login_user.post(self.url, data={'title': title})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('title') == title

        board_participant = BoardParticipant.objects.get(user_id=current_user.id)

        assert board_participant.role == BoardParticipant.Role.owner

    def test_board_create_permission_denied(self, api_client, faker):
        title = faker.text(max_nb_chars=255)

        response = api_client.post(self.url, data={'title': title})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}


@pytest.mark.django_db
class TestBoardList:
    url = reverse('board-list')

    def test_get_board_list_permission_denied(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_get_list_available_boards(self, current_user, board_factory, login_user,
                                       user_factory, board_participant_factory):
        board_factory.create_batch(2, owner=current_user)
        another_user: User = user_factory.create()
        board_another_user: Board = board_factory.create(owner=another_user)
        board_participant_factory.create(user=current_user, board=board_another_user)

        response = login_user.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 3

    def test_get_list_another_user_boards(self, current_user, board_factory, login_user,
                                          user_factory, board_participant_factory):
        another_user: User = user_factory.create()
        board_another_user = board_factory.create_batch(2, owner=another_user)

        response = login_user.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

        board_factory.create_batch(2, owner=current_user)
        board_participant_factory.create(user=current_user, board=board_another_user[0])

        response = login_user.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 3


@pytest.mark.django_db
class TestBoard:
    def test_get_board_success(self, current_user, board_factory, login_user):
        board = board_factory.create(owner=current_user)
        url = reverse('board-retrieve', args=[board.id])
        response = login_user.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == BoardSerializer(board).data

    def test_get_another_user_board(self, current_user, board_factory, login_user, user_factory):
        another_user: User = user_factory.create()
        board_another_user = board_factory.create(owner=another_user)
        url = reverse('board-retrieve', args=[board_another_user.id])

        response = login_user.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not found.'}

    def test_get_board_failed(self, api_client, board_factory, current_user):
        board = board_factory.create(owner=current_user)
        url = reverse('board-retrieve', args=[board.id])

        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}