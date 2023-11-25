from django.test import TestCase


class SerializerTest(TestCase):

    @staticmethod
    def get_fields(serializer, *, only_names=False) -> dict | list[str]:
        serializer = serializer()
        if only_names:
            return list(serializer.get_fields().keys())
        return serializer.get_fields()

    @staticmethod
    def get_field(serializer, field_name: str):
        return serializer().get_fields()[field_name]