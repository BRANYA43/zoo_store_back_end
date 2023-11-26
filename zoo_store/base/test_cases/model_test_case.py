from base.test_cases.test_case import TestCase


class ModelTestCase(TestCase):
    @staticmethod
    def get_field(model, field_name: str):
        return model._meta.get_field(field_name)

    @staticmethod
    def get_fields(model, *, only_names=False) -> list[str]:
        fields = model._meta.fields
        if only_names:
            return [field.name for field in fields]
        return fields

    @staticmethod
    def get_meta_attr(model, attr_name: str):
        return getattr(model._meta, attr_name)
