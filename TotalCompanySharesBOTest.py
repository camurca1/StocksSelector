import unittest
from TotalCompanySharesBO import TotalCompanySharesBO


class StocksLiquidityBOTest(unittest.TestCase):
    def test_TotalSharesCalc(self):
        total_shares = TotalCompanySharesBO()
        self.assertTrue(total_shares.FINAL_CSV_PATH.exists())


if __name__ == '__main__':
    unittest.main()
