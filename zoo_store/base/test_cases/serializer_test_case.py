from base.test_cases.test_case import TestCase


class SerializerTestCase(TestCase):
    @staticmethod
    def get_field(serializer, field_name: str):
        return serializer().fields[field_name]

    @staticmethod
    def get_field_names(serializer):
        return list(serializer().fields)
