import unittest
from FREParser import FREParser
from pathlib import Path


class CompanyFinancialReportsTests(unittest.TestCase):

    def test_CompanyReferenceFormBO(self):
        company_info = FREParser()
        self.assertTrue(Path(company_info.FRE_PATH).exists())


if __name__ == '__main__':
    unittest.main()
