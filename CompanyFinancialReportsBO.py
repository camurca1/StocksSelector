########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 2022-08-18                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: ETL dos relatórios financeiros                                                                                       #
########################################################################################################################
from BaseBO import BaseBO
from pathlib import Path
from datetime import datetime
import pandas as pd
import wget
from zipfile import ZipFile


class CompanyFinancialReportsBO(BaseBO):
    def __init__(self):
        super(BaseBO, self).__init__()
        self.FILE_URL = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/'
        self.CSV_FILE_NAME = ''
        self.HDF_FILE_NAME = ''
        self.RAW_FILE_NAME = ''
        self.TARGET_PATH = Path.cwd() / 'data' / 'financial_reports'
        self.EXTRACT_PATH = self.TARGET_PATH / 'CompaniesFinancialReports'
        self.FINAL_RAW_PATH = self.TARGET_PATH
        self.FINAL_CSV_PATH = self.TARGET_PATH / 'DFP_forms'
        self.FINAL_HDF_PATH = self.TARGET_PATH / 'DFP_forms'
        self.REPORT_TYPES = ['BPA_con', 'BPP_con', 'DRE_con', 'DFC_MI_con']
        self.INITIAL_YEAR = datetime.now().year - 10
        self.FINAL_YEAR = datetime.now().year
        self.company_data = None
        self.company_transformed_data = []

        self.__initializer()

    def __initializer(self):
        if not self.check_if_resource_exists(self.FINAL_CSV_PATH):
            try:
                self.create_destination_path(self.TARGET_PATH)
                self.create_destination_path(self.EXTRACT_PATH)
                self.create_destination_path(self.FINAL_CSV_PATH)
            except FileExistsError:
                pass  # insert log exception
            finally:
                if self.check_download_url(self.FILE_URL) < 400:
                    self._get_resource()
                    self._transform_resource()
                    self._save_resource()
                else:
                    self.company_transformed_data = pd.read_csv(self.FINAL_CSV_PATH)

    def _get_resource(self):
        zip_files = []

        for year in range(self.INITIAL_YEAR, self.FINAL_YEAR):
            zip_files.append(f'dfp_cia_aberta_{year}.zip')

        for file in zip_files:
            self.RAW_FILE_NAME = file
            self.FINAL_RAW_PATH = Path.joinpath(self.TARGET_PATH, self.RAW_FILE_NAME)

            if not self.check_if_resource_exists(self.FINAL_RAW_PATH):
                url = f'{self.FILE_URL}{file}'
                wget.download(url, str(self.TARGET_PATH))
                ZipFile(self.FINAL_RAW_PATH, 'r').extractall(self.EXTRACT_PATH)
                Path.unlink(self.FINAL_RAW_PATH)

    def _transform_resource(self):
        for report in self.REPORT_TYPES:
            self.company_data = pd.DataFrame()
            for year in range(self.INITIAL_YEAR, self.FINAL_YEAR):
                self.FINAL_RAW_PATH = self.TARGET_PATH / 'CompaniesFinancialReports' / f'dfp_cia_aberta_{report}_{year}.csv'
                if not self.check_if_resource_exists(self.FINAL_RAW_PATH):
                    self.company_data = pd.concat([self.company_data, pd.read_csv(self.FINAL_RAW_PATH,
                                                                                  sep=';',
                                                                                  decimal=',',
                                                                                  encoding='ISO-8859-1')])
            if not self.check_if_resource_exists(self.FINAL_RAW_PATH):
                self.company_transformed_data.append(FinancialReportDTO(report, self.company_data))

    def _save_resource(self):
        for data in self.company_transformed_data:
            self.FINAL_CSV_PATH = self.TARGET_PATH / 'DFP_forms' / f'companies_{data.report_type}_{self.INITIAL_YEAR}_{self.FINAL_YEAR}.csv'
            if not self.check_if_resource_exists(self.FINAL_CSV_PATH):
                data.data.to_csv(self.FINAL_CSV_PATH, index=False)


class FinancialReportDTO:
    def __init__(self, report_type, data):
        self.report_type = report_type
        self.data = data
