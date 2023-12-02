from unittest.mock import Mock

from base.test_cases import ModelTestCase, SerializerTestCase, ViewSetTestCase
from base.test_cases.test_case import TestCase
from base.test_cases.view_set_test_case import (
    INCORRECT_VALUE_ERROR_MSG,
    NOT_ANONYMOUS_ERROR_MSG,
    NOT_AUTHENTICATED_ERROR_MSG,
    NOT_MATCH_STATUS_CODE_ERROR_MSG,
    NOT_STAFF_ERROR_MSG,
)
from django.db import models
from rest_framework import serializers, status


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
            field2 = models.IntegerField()

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


class SerializerTestCaseTest(SerializerTestCase):
    def setUp(self) -> None:
        class Serializer(serializers.Serializer):
            field1 = serializers.Field()
            field2 = serializers.Field()

        self.Serializer = Serializer

    def test_get_field_gets_correct_field(self):
        field = self.get_field(self.Serializer, 'field1')
        self.assertIsInstance(field, serializers.Field)
        self.assertEqual(field.field_name, 'field1')

    def test_get_fields_gets_correct_field_name_list(self):
        fields = self.get_field_names(self.Serializer)
        expected_fields = list(self.Serializer().fields)
        self.assertSequenceEqual(fields, expected_fields)


class ViewTestCaseTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.mock_response = Mock()

    def test_assertStatusCodeEqual(self):
        self.mock_response.status_code = status.HTTP_200_OK

        self.assertStatusCodeEqual(self.mock_response, status.HTTP_200_OK)

    def test_assertStatusCodeEqual_raise_error(self):
        self.mock_response.status_code = status.HTTP_404_NOT_FOUND

        with self.assertRaisesRegexp(AssertionError, NOT_MATCH_STATUS_CODE_ERROR_MSG):
            self.assertStatusCodeEqual(self.mock_response, status.HTTP_200_OK)

    def test_assertUserIs_raise_error_if_incorrect_value_is_user_is(self):
        with self.assertRaisesRegexp(AssertionError, INCORRECT_VALUE_ERROR_MSG):
            self.assertUserIs(self.mock_response, 'icorrect_value')

    def test_assertUserIs_valid_if_user_is_anonymous(self):
        self.mock_response.wsgi_request.user.is_anonymous = True
        self.assertUserIs(self.mock_response, 'anonymous')

    def test_assertUserIs_raise_error_if_user_is_not_anonymous(self):
        self.mock_response.wsgi_request.user.is_anonymous = False

        with self.assertRaisesRegexp(AssertionError, NOT_ANONYMOUS_ERROR_MSG):
            self.assertUserIs(self.mock_response, 'anonymous')

    def test_assertUserIs_valid_if_user_is_authenticated(self):
        self.mock_response.wsgi_request.user.is_authenticated = True
        self.assertUserIs(self.mock_response, 'authenticated')

    def test_assertUserIs_raise_error_if_user_is_not_authenticated(self):
        self.mock_response.wsgi_request.user.is_authenticated = False

        with self.assertRaisesRegexp(AssertionError, NOT_AUTHENTICATED_ERROR_MSG):
            self.assertUserIs(self.mock_response, 'authenticated')

    def test_assertUserIs_valid_if_user_is_staff(self):
        self.mock_response.wsgi_request.user.is_staff = True
        self.assertUserIs(self.mock_response, 'staff')

    def test_assertUserIs_raise_error_if_user_is_not_staff(self):
        self.mock_response.wsgi_request.user.is_staff = False

        with self.assertRaisesRegexp(AssertionError, NOT_STAFF_ERROR_MSG):
            self.assertUserIs(self.mock_response, 'staff')
