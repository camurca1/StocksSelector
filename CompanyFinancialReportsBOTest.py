import unittest
from CompanyFinancialReportsBO import CompanyFinancialReportsBO
from pathlib import Path


class CompanyFinancialReportsTests(unittest.TestCase):

    def test_CompanyFinancialReportsBO(self):
        company_info = CompanyFinancialReportsBO()
        self.assertTrue(Path(company_info.FINAL_CSV_PATH).exists())


if __name__ == '__main__':
    unittest.main()
