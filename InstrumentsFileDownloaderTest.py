import unittest
from InstrumentsFileDownloader import InstrumentsFileDownloader


class CompanyFinancialReportsTests(unittest.TestCase):

    def test_CompanyReferenceFormBO(self):
        instruments = InstrumentsFileDownloader()

        self.assertTrue(instruments.DOWNLOAD_PATH.exists())


if __name__ == '__main__':
    unittest.main()
