import unittest
from CompanyStockPricesBO import CompanyStockPricesBO


class CompanyStockPricesBOTest(unittest.TestCase):

    def test_HandlerInit(self):
        prices = CompanyStockPricesBO()
        self.assertTrue(prices.TARGET_PATH.exists())


if __name__ == '__main__':
    unittest.main()
