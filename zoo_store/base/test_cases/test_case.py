from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):
    def assertFieldNamesEqual(self, first: list[str], second: list[str], msg=None):
        first.sort()
        second.sort()

        self.assertListEqual(first, second, msg)

    @staticmethod
    def get_meta_attr(model, attr_name: str):
        return getattr(model._meta, attr_name)
