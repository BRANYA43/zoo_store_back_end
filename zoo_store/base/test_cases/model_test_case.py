from typing import Type, TypeVar

from base.test_cases.test_case import TestCase
from django.db.models import Field, Model

FieldType = TypeVar('FieldType', bound=Field)


class ModelTestCase(TestCase):
    @staticmethod
    def get_field(model: Type[Model], name: str) -> Type[Field]:
        """
        Returns the model field by name.
        :param model: The django model from which to retrieve the field.
        :param name: The name of the model field.
        """
        return model._meta.get_field(name)

    @staticmethod
    def get_fields(model: Type[Model], *, only_names=False) -> list[Type[Field]] | list[str]:
        """
        Returns the list of all model fields or field names.
        :param model:  The django model from which to retrieve the fields.
        :param only_names: The flag, that defines whether to return the list of model names.
        """
        fields = model._meta.fields
        if only_names:
            return [field.name for field in fields]
        return fields
