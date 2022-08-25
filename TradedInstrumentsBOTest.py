import unittest
from TradedInstrumentsBO import TradedInstrumentsBO


class TradedInstruments(unittest.TestCase):

    def test_CompanyReferenceFormBO(self):
        instruments = TradedInstrumentsBO()

        self.assertTrue(instruments.ISIN_ZIP_PATH.exists())


if __name__ == '__main__':
    unittest.main()
