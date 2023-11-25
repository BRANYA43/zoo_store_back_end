from accounts.models import Profile
from accounts.tests import create_test_user
from django.test import TestCase


class CreatedUserSignalTest(TestCase):
    def test_signals_create_profile_after_creating_user(self):
        user = create_test_user()

        self.assertEqual(Profile.objects.count(), 1)

        profile_user = Profile.objects.first().user

        self.assertEqual(profile_user.uuid, user.uuid)

    @staticmethod
    def test_signals_dont_create_profile_if_user_has_profile():
        user = create_test_user()

        user.email = 'rick.sanchez@example.com'
        user.save()  # Not raises
