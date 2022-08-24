import unittest
from ISINDownloader import ISINDownloader


class CompanyFinancialReportsTests(unittest.TestCase):

    def test_CompanyReferenceFormBO(self):
        isin = ISINDownloader()

        self.assertTrue(isin.DOWNLOAD_PATH.exists())


if __name__ == '__main__':
    unittest.main()