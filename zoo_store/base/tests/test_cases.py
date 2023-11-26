from base.test_cases.test_case import TestCase


class TestCaseTest(TestCase):
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


