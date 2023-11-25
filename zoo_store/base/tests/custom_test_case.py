from django.test import TestCase


class CustomTestCase(TestCase):
    def assert_field_lists_equal(self, first: list[str], second: list[str]):
        first.sort()
        second.sort()

        self.assertListEqual(first, second)
