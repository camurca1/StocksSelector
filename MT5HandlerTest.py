import unittest
from MT5Handler import Mt5Handler


class MT5HandlerTest(unittest.TestCase):

    def test_HandlerInit(self):
        mt5 = Mt5Handler()
        self.assertTrue(mt5.MAGIC_NUMBER == 234000)


if __name__ == '__main__':
    unittest.main()
