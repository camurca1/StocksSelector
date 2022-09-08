import unittest
from B3DateValidator import B3DateValidator


class B3DateValidatorTest(unittest.TestCase):
    def test_DateValidator(self):
        date = B3DateValidator('2022-09-07')
        self.assertTrue(date.valid_date.strftime('%Y-%m-%d') == '2022-09-06')


if __name__ == '__main__':
    unittest.main()
