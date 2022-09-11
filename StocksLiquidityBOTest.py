import unittest
from StocksLiquidityBO import StocksLiquidityBO


class StocksLiquidityBOTest(unittest.TestCase):
    def test_LiquidityCalc(self):
        stock_liquidity = StocksLiquidityBO()
        self.assertTrue(stock_liquidity.FINAL_CSV_PATH.exists())  # add assertion here


if __name__ == '__main__':
    unittest.main()
