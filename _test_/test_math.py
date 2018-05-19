import unittest
from faker import Faker
from odd_number import OddNumber


class MathTestCase(unittest.TestCase):

    def setUp(self):
        self.fake = Faker()

    def test_odd_number_not_none(self):
        test_number = self.fake.random_number()
        is_odd_number = OddNumber.odd_number(test_number)
        self.assertIsNotNone(is_odd_number)

    def test_odd_number_is_tre(self):
        test_number = self.fake.random_number() * 2
        is_odd_number = OddNumber.odd_number(test_number)
        self.assertEquals(is_odd_number, True)

    def test_odd_number_is_false(self):
        test_number = self.fake.random_number() * 2 + 1
        is_odd_number = OddNumber.odd_number(test_number)
        self.assertEquals(is_odd_number, False)