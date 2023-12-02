from unittest.mock import patch

from accounts.serializers import ProfileSerializer
from accounts.tests import create_test_user
from base.test_cases import ViewSetTestCase
from rest_framework import status
from rest_framework.reverse import reverse


@patch('rest_framework.relations.HyperlinkedRelatedField.to_representation', return_value='mocked_url')
class ProfileRetrieveViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.client.force_authenticate(self.user)
        self.url = reverse('profile-detail', args=[self.user.profile.uuid])
        self.serializer_class = ProfileSerializer

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
        expected_data = self.serializer_class(self.user.profile, context=context).data

        response = self.client.get(self.url)

        self.assertSequenceEqual(response.data, expected_data)


@patch('rest_framework.relations.HyperlinkedRelatedField.to_representation', return_value='mocked_url')
class ProfileUpdateViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.client.force_authenticate(self.user)
        self.url = reverse('profile-detail', args=[self.user.profile.uuid])
        self.serializer_class = ProfileSerializer
        self.data = {'first_name': 'Rick', 'last_name': 'Sanchez'}

    def test_view_is_not_available_for_anonymous_user(self, mock):
        self.client.logout()

        response = self.client.patch(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_401_UNAUTHORIZED)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_not_available_for_not_owner(self, mock):
        not_owner = create_test_user(email='morty@test.com')
        self.client.force_authenticate(not_owner)

        response = self.client.patch(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_403_FORBIDDEN)
        self.assertUserIs(response, 'authenticated')

    def test_view_is_available_for_owner(self, mock):
        response = self.client.patch(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'authenticated')

    def test_view_is_available_for_staff_user(self, mock):
        self.user.is_staff = True
        self.user.save()

        response = self.client.patch(self.url, self.data, patrial=True, format='json')

        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertUserIs(response, 'staff')

    def test_view_updates_chosen_user(self, mock):
        response = self.client.patch(self.url, self.data, patrial=True, format='json')
        self.user.profile.refresh_from_db()
        context = {'request': self.get_fake_request(self.url)}
        expected_data = self.serializer_class(self.user.profile, context=context).data

        self.assertSequenceEqual(response.data, expected_data)