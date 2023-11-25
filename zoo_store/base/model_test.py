from django.test import TestCase


class ModelTest(TestCase):
    @staticmethod
    def get_field(model, field_name: str):
        return model._meta.get_field(field_name)

    @staticmethod
    def get_fields(model, *, only_name=False) -> list | list[str]:
        fields = model._meta.fields

        if only_name:
            return [field.name for field in fields]

        return fields

    @staticmethod
    def get_meta_attr(model, attr_name: str):
        return getattr(model._meta, attr_name)