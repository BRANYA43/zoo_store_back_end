from unittest.mock import patch

from accounts.serializers import UserSerializer
from accounts.tests import create_test_user
from base.test_cases.view_set_test_case import ViewSetTestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

User = get_user_model()


@patch('rest_framework.relations.HyperlinkedRelatedField.to_representation', return_value='mocked_url')
class UserListViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.client.force_authenticate(self.user)
        self.url = reverse('user-list')
        self.serializer_class = UserSerializer

    def test_view_is_not_available_for_anonymous_user(self, mock):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_401_UNAUTHORIZED)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_available_for_owner(self, mock):
        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'authenticated')

    def test_view_is_available_for_staff_user(self, mock):
        self.user.is_staff = True
        self.user.save()

        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'staff')

    def test_view_returns_user_list(self, mock):
        for i in range(3):
            create_test_user(email=f'user{i}@test.com')
        context = {'request': self.get_fake_request(self.url)}
        expected_data = self.serializer_class(User.objects.all(), context=context, many=True).data

        response = self.client.get(self.url)

        self.assertSequenceEqual(response.data, expected_data)


@patch('rest_framework.relations.HyperlinkedRelatedField.to_representation', return_value='mocked_url')
class UserRetrieveViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.client.force_authenticate(self.user)
        self.url = reverse('user-detail', args=[self.user.uuid])
        self.serializer_class = UserSerializer

    def test_view_is_not_available_for_anonymous_user(self, mock):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_401_UNAUTHORIZED)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_not_available_for_not_owner(self, mock):
        not_owner = create_test_user(email='morty@test.com')
        self.client.force_authenticate(not_owner)

        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_403_FORBIDDEN)
        self.assertUserIs(response, 'authenticated')

    def test_view_is_available_for_owner(self, mock):
        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'authenticated')

    def test_view_is_available_for_staff_user(self, mock):
        self.user.is_staff = True
        self.user.save()

        response = self.client.get(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'staff')

    def test_view_returns_correct_user(self, mock):
        context = {'request': self.get_fake_request(self.url)}
        expected_data = self.serializer_class(self.user, context=context).data

        response = self.client.get(self.url)

        self.assertSequenceEqual(response.data, expected_data)


@patch('rest_framework.relations.HyperlinkedRelatedField.to_representation', return_value='mocked_url')
class UserUpdateViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.client.force_authenticate(self.user)
        self.url = reverse('user-detail', args=[self.user.uuid])
        self.data = {'is_active': True}

    def test_view_is_not_available_for_anonymous_user(self, mock):
        self.client.logout()

        response = self.client.put(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_401_UNAUTHORIZED)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_not_available_for_not_owner(self, mock):
        not_owner = create_test_user(email='morty@test.com')
        self.client.force_authenticate(not_owner)

        response = self.client.put(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_403_FORBIDDEN)
        self.assertUserIs(response, 'authenticated')

    def test_view_is_available_for_owner(self, mock):
        response = self.client.put(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'authenticated')

    def test_view_is_available_for_staff_user(self, mock):
        self.user.is_staff = True
        self.user.save()

        response = self.client.put(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'staff')

    def test_view_updates_chosen_user(self, mock):
        response = self.client.put(self.url, self.data, patrial=True, format='json')
        context = {'request': self.get_fake_request(self.url)}
        expected_data = UserSerializer(self.user, context=context).data

        self.assertSequenceEqual(response.data, expected_data)


class UserDestroyViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.client.force_authenticate(self.user)
        self.url = reverse('user-detail', args=[self.user.uuid])

    def test_view_is_not_available_for_anonymous_user(self):
        self.client.logout()

        response = self.client.delete(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_401_UNAUTHORIZED)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_not_available_for_not_owner(self):
        not_owner = create_test_user(email='morty@test.com')
        self.client.force_authenticate(not_owner)

        response = self.client.delete(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_403_FORBIDDEN)
        self.assertUserIs(response, 'authenticated')

    def test_view_is_available_for_owner(self):
        response = self.client.delete(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_204_NO_CONTENT)
        self.assertUserIs(response, 'authenticated')

    def test_view_is_available_for_staff_user(self):
        self.user.is_staff = True
        self.user.save()

        response = self.client.delete(self.url)

        self.assertStatusCodeEqual(response, status.HTTP_204_NO_CONTENT)
        self.assertUserIs(response, 'staff')

    def test_view_deletes_chosen_user(self):
        self.assertEqual(User.objects.count(), 1)

        self.client.delete(self.url)

        self.assertEqual(User.objects.count(), 0)
