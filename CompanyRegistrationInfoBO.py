########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 2022-08-18                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: ETL dos dados registrados na CVM                                                                             #
########################################################################################################################
from BaseBO import BaseBO
from pathlib import Path
import pandas as pd


class CompanyRegistrationInfoBO(BaseBO):
    def __init__(self):
        self.FILE_URL = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv'
        self.CSV_FILE_NAME = 'RegularCompaniesRegistrationInfo.csv'
        self.HDF_FILE_NAME = 'RegularCompaniesRegistrationInfo.hdf'
        self.TARGET_PATH = Path.cwd() / 'data' / 'companies'
        self.FINAL_CSV_PATH = self.TARGET_PATH / self.CSV_FILE_NAME
        self.FINAL_HDF_PATH = self.TARGET_PATH / self.HDF_FILE_NAME
        self.company_data = None
        self.company_transformed_data = None

        self.__initializer()

    def __initializer(self):
        if not self.check_if_resource_exists(self.FINAL_CSV_PATH):
            self.create_destination_path(self.TARGET_PATH)

            if self.check_download_url(self.FILE_URL) < 400:
                self._get_resource()
                self._transform_resource()
                self._save_resource()
        else:
            self.company_transformed_data = pd.read_csv(self.FINAL_CSV_PATH)

    def _get_resource(self):
        self.company_data = pd.read_csv(self.FILE_URL, sep=';', encoding='WINDOWS-1252')

    def _transform_resource(self):
        self.company_transformed_data = self.company_data[self.company_data['SIT'] == 'ATIVO']
        self.company_transformed_data = self.company_transformed_data[self.company_transformed_data['TP_MERC'] != 'BALCÃO ORGANIZADO']
        self.company_transformed_data = self.company_transformed_data[self.company_transformed_data['TP_MERC'] != 'BALCÃO NÃO ORGANIZADO']
        self.company_transformed_data = self.company_transformed_data[self.company_transformed_data['SIT_EMISSOR'].isin(['FASE OPERACIONAL', 'FASE PRÉ-OPERACIONAL'])]
        self.company_transformed_data = self.company_transformed_data.drop_duplicates()
        self.company_transformed_data['CD_CVM'] = self.company_transformed_data['CD_CVM'].astype(int)
        self.company_transformed_data.reset_index(drop=True, inplace=True)

    def _save_resource(self):
        self.company_transformed_data.to_csv(self.FINAL_CSV_PATH, index=False)
