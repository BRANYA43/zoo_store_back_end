from base.test_cases import ModelTestCase
from base.test_cases.test_case import TestCase
from django.db import models


class TestCaseTest(TestCase):
    def setUp(self) -> None:
        class Model(models.Model):
            class Meta:
                abstract = True

        self.Model = Model

    def test_get_meta_attr_gets_correct_attr(self):
        self.assertTrue(self.get_meta_attr(self.Model, 'abstract'))

    def test_assertFieldNamesEqual_doesnt_raise_error(self):
        fields1 = ['1', '2', '3']
        fields2 = ['3', '2', '1']

        self.assertFieldNamesEqual(fields1, fields2)  # doesn't raise error

    def test_assertFieldNamesEqual_raises_error_if_fields_dont_have_the_same_length(self):
        fields1 = ['1', '2', '3']
        fields2 = ['2', '1']

        with self.assertRaises(AssertionError):
            self.assertFieldNamesEqual(fields1, fields2)

    def test_assertFieldNamesEqual_raises_error_if_fields_dont_have_the_same_names(self):
        fields1 = ['1', '2', '3']
        fields2 = ['4', '2', '1']

        with self.assertRaises(AssertionError):
            self.assertFieldNamesEqual(fields1, fields2)


class ModelTestCaseTest(ModelTestCase):

    def setUp(self) -> None:
        class Model(models.Model):
            field1 = models.Field()
            field2 = models.Field()

            class Meta:
                abstract = True

        self.Model = Model

    def test_get_field_gets_correct_field(self):
        field = self.get_field(self.Model, 'field1')
        self.assertIsInstance(field, models.Field)
        self.assertEqual(field.name, 'field1')

    def test_get_fields_gets_correct_field_list(self):
        fields = self.get_fields(self.Model)
        expected_fields = self.Model._meta.fields
        self.assertSequenceEqual(fields, expected_fields)

    def test_get_fields_gets_correct_field_name_list(self):
        fields = self.get_fields(self.Model, only_names=True)
        expected_fields = [field.name for field in self.Model._meta.fields]
        self.assertSequenceEqual(fields, expected_fields)

    def test_get_meta_attr_gets_correct_attr(self):
        self.assertTrue(self.get_meta_attr(self.Model, 'abstract'))