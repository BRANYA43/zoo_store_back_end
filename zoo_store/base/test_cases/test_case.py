from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):
    def assertFieldNamesEqual(self, first: list[str], second: list[str], msg=None):
        first.sort()
        second.sort()

        self.assertListEqual(first, second, msg)
