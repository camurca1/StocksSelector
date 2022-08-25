import unittest
from ISINDownloader import ISINDownloader


class ISINDownloaderTests(unittest.TestCase):

    def test_CompanyReferenceFormBO(self):
        isin = ISINDownloader()

        self.assertTrue(isin.FINAL_ISIN_FILE.exists())


if __name__ == '__main__':
    unittest.main()
