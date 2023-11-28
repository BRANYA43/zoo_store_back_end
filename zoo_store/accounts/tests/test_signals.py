from accounts.models import Profile
from accounts.tests import create_test_user
from base.test_cases.test_case import TestCase


class CreatedUserSignalTest(TestCase):
    def test_signal_creates_profile_after_creating_user(self):
        user = create_test_user()
        self.assertEqual(Profile.objects.count(), 1)

        profile = Profile.objects.first()
        self.assertEqual(profile.user.uuid, user.uuid)

    def test_signal_doesnt_create_profile_if_user_has_profile(self):
        user = create_test_user()
        profile = Profile.objects.first()

        user.save()  # doesn't raises error

        self.assertEqual(profile.uuid, user.profile.uuid)