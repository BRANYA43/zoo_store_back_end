from typing import Type

from base.test_cases.test_case import TestCase
from rest_framework.fields import Field
from rest_framework.serializers import Serializer


class SerializerTestCase(TestCase):
    @staticmethod
    def get_field(serializer: Type[Serializer], name: str) -> Type[Field]:
        """
        Returns the serializer field by name.
        :param serializer: The rest serializer from which to retrieve the field.
        :param name: The name of the serializer field.
        """
        return serializer().fields[name]

    @staticmethod
    def get_field_names(serializer: Type[Serializer]) -> list[str]:
        """
        Returns the list of all serializer field names.
        :param serializer:  The rest serializer from which to retrieve the field.
        """
        return list(serializer().fields)
