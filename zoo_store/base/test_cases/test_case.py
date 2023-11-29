from typing import Any, Type

from django.db.models import Model
from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):
    def assertFieldNamesEqual(self, first: list[str], second: list[str], msg=None):
        """
        Validates whether first list field names is equal with second list field names.
        :param first: List of field names to compare.
        :param second: List of field names for comparison.
        :param msg: Optional message to include in the failure message.
        """
        first.sort()
        second.sort()

        self.assertListEqual(first, second, msg)

    @staticmethod
    def get_meta_attr(model: Type[Model], name: str) -> Any:
        """
        Returns the meta attribute of the model.
        :param model: The django model from which to retrieve meta attribute.
        :param name: The name of meta attribute.
        """
        return getattr(model._meta, name)
