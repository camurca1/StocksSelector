import unittest
from CompanyReferenceFormBO import CompanyReferenceFormBO
from pathlib import Path


class CompanyFinancialReportsTests(unittest.TestCase):

    def test_CompanyReferenceFormBO(self):
        company_info = CompanyReferenceFormBO()
        self.assertTrue(Path(company_info.FINAL_CSV_PATH).exists())


if __name__ == '__main__':
    unittest.main()