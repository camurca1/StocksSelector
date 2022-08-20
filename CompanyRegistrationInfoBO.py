########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 2022-08-18                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: Arquivo de configuração                                                                                      #
########################################################################################################################
from pathlib import Path
from requests import head
import pandas as pd


class CompanyRegistrationInfoBO:
    def __init__(self):
        self.FILE_URL = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv'
        self.TARGET_PATH = Path.cwd() / 'data' / 'companies'
        self.FILE_NAME = 'CompanyRegistrationInfo.csv'
        self.FINAL_PATH = self.TARGET_PATH / self.FILE_NAME
        self.company_data = None
        self.company_cleaned_data = None

        if not self.check_if_resource_exists(self.TARGET_PATH):
            self.create_destination_path()

    @classmethod
    def check_if_resource_exists(cls, path):
        return Path(path).exists()

    def create_destination_path(self):
        try:
            self.TARGET_PATH.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print("Folder is already there")
        else:
            print("Folder was created")

    def check_download_url(self):
        response = head(self.FILE_URL)
        return response.status_code

    def get_resource(self):
        self.company_data = pd.read_csv(self.FILE_URL, sep=';', encoding='WINDOWS-1252')

    def clean_resource(self):
        self.company_cleaned_data = self.company_data[self.company_data['SIT'] == 'ATIVO']
        self.company_cleaned_data = self.company_cleaned_data[self.company_cleaned_data['TP_MERC'] != 'BALCÃO ORGANIZADO']
        self.company_cleaned_data = self.company_cleaned_data[self.company_cleaned_data['TP_MERC'] != 'BALCÃO NÃO ORGANIZADO']
        self.company_cleaned_data = self.company_cleaned_data[self.company_cleaned_data['SIT_EMISSOR'].isin(['FASE OPERACIONAL', 'FASE PRÉ-OPERACIONAL'])]
        self.company_cleaned_data.reset_index(drop=True, inplace=True)

    def save_resource(self):
        self.company_cleaned_data.to_csv(self.FINAL_PATH, index=False)
