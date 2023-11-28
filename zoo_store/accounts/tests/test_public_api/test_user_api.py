from unittest.mock import patch

from accounts.serializers import UserCreateSerializer, UserSerializer
from accounts.tests import create_test_user
from base.test_cases.view_set_test_case import ViewSetTestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

User = get_user_model()


@patch('rest_framework.relations.HyperlinkedRelatedField.to_representation', return_value='mocked_url')
class UserListViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.url = reverse('user-list')
        self.serializer_class = UserSerializer

    def test_view_is_available_for_anonymous_user(self, mock):
        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_available_for_authenticated_user(self, mock):
        user = create_test_user()
        self.client.force_authenticate(user)

        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'authenticated')

    def test_view_returns_user_list(self, mock):
        for i in range(3):
            create_test_user(email=f'user{i}@test.com')
        context = {'request': self.get_request(self.url)}
        expected_data = self.serializer_class(User.objects.all(), context=context, many=True).data

        response = self.client.get(self.url)

        self.assertSequenceEqual(response.data, expected_data)


@patch('rest_framework.relations.HyperlinkedRelatedField.to_representation', return_value='mocked_url')
class UserRetrieveViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.url = reverse('user-detail', args=[self.user.uuid])
        self.serializer_class = UserSerializer

    def test_view_is_available_for_anonymous_user(self, mock):
        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_available_for_authenticated_user(self, mock):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'authenticated')

    def test_view_returns_correct_user(self, mock):
        context = {'request': self.get_request(self.url)}
        expected_data = self.serializer_class(self.user, context=context).data

        response = self.client.get(self.url)

        self.assertSequenceEqual(response.data, expected_data)


class UserCreateViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
        }
        self.url = reverse('user-list')

    def test_view_is_available_for_anonymous_user(self):
        response = self.client.post(self.url, self.data)

        self.assertStatusCodeEqual(response, status.HTTP_201_CREATED)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_available_for_authenticated_user(self):
        user = create_test_user('morty@test.com', 'qwe123!@#')
        self.client.force_authenticate(user)

        response = self.client.post(self.url, self.data)

        self.assertStatusCodeEqual(response, status.HTTP_201_CREATED)
        self.assertUserIs(response, 'authenticated')

    def test_view_creates_user_by_email_and_password(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        self.assertEqual(response.data['uuid'], str(user.uuid))

    def test_view_uses_UserCreateSerializer(self):
        response = self.client.post(self.url, self.data)

        user = User.objects.first()
        context = {'request': self.get_request(self.url)}
        expected_data = UserCreateSerializer(user, context=context).data

        self.assertSequenceEqual(response.data, expected_data)


@patch('rest_framework.relations.HyperlinkedRelatedField.to_representation', return_value='mocked_url')
class UserUpdateViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.url = reverse('user-detail', args=[self.user.uuid])
        self.data = {'is_active': True}

    def test_view_is_available_for_anonymous_user(self, mock):
        response = self.client.put(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_available_for_authenticated_user(self, mock):
        self.client.force_authenticate(self.user)

        response = self.client.put(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'authenticated')

    def test_view_updates_chosen_user(self, mock):
        response = self.client.put(self.url, self.data, patrial=True, format='json')
        context = {'request': self.get_request(self.url)}
        expected_data = UserSerializer(self.user, context=context).data

        self.assertSequenceEqual(response.data, expected_data)


class UserDestroyViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.url = reverse('user-detail', args=[self.user.uuid])

    def test_view_is_available_for_anonymous_user(self):
        response = self.client.delete(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_204_NO_CONTENT)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_available_for_authenticated_user(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_204_NO_CONTENT)
        self.assertUserIs(response, 'authenticated')

    def test_view_deletes_chosen_user(self):
        self.assertEqual(User.objects.count(), 1)

        self.client.delete(self.url)

        self.assertEqual(User.objects.count(), 0)
