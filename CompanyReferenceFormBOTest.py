import unittest
from CompanyReferenceFormBO import CompanyReferenceFormBO


class CompanyFinancialReportsTests(unittest.TestCase):

    def test_CompanyReferenceFormBO(self):
        company_info = CompanyReferenceFormBO()

        self.assertTrue(company_info is not None)


if __name__ == '__main__':
    unittest.main()
