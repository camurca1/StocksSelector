import unittest
from CompanyRegistrationInfoBO import CompanyRegistrationInfoBO
from pathlib import Path


class CompanyRegistrationDataTests(unittest.TestCase):

    def test_CompanyRegistrationInfoBO(self):
        company_info = CompanyRegistrationInfoBO()
        self.assertTrue(Path(company_info.FINAL_PATH).exists())


if __name__ == '__main__':
    unittest.main()
