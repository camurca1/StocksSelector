import unittest
from TotalCompanySharesBO import TotalCompanySharesBO


class StocksLiquidityBOTest(unittest.TestCase):
    def test_TotalSharesCalc(self):
        total_shares = TotalCompanySharesBO()
        # self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
