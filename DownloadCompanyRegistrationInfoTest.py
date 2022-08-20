import unittest
from CompanyRegistrationInfoBO import CompanyRegistrationInfoBO


class CompanyRegistrationDataTests(unittest.TestCase):

    def test_check_if_company_data_directory_exists(self):
        company_info = CompanyRegistrationInfoBO()
        self.assertTrue(company_info.check_if_resource_exists(company_info.TARGET_PATH))

    def test_check_if_company_data_file_exists(self):
        company_info = CompanyRegistrationInfoBO()
        company_info.get_resource()
        company_info.clean_resource()
        company_info.save_resource()
        self.assertTrue(company_info.check_if_resource_exists(company_info.FINAL_PATH))

    def test_do_url_check(self):
        company_info = CompanyRegistrationInfoBO()
        self.assertTrue(company_info.check_download_url() < 400)

    def test_get_resource(self):
        company_info = CompanyRegistrationInfoBO()
        company_info.get_resource()
        self.assertTrue(company_info.company_data is not None)

    def test_clean_resource(self):
        company_info = CompanyRegistrationInfoBO()
        company_info.get_resource()
        company_info.clean_resource()
        self.assertTrue(company_info.company_cleaned_data is not None)


if __name__ == '__main__':
    unittest.main()
