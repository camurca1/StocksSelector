########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 2022-08-18                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: ETL dos formulários de referência                                                                                    #
########################################################################################################################
from BaseBO import BaseBO
from pathlib import Path
from datetime import datetime
import pandas as pd
import wget
from zipfile import ZipFile
import requests
from io import BytesIO


class CompanyReferenceFormBO(BaseBO):
    def __init__(self):
        super(BaseBO, self).__init__()
        self.ZIP_FILE_URL = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FRE/DADOS/'
        self.XML_FILE_URL = ''
        self.CSV_FILE_NAME = ''
        self.HDF_FILE_NAME = ''
        self.RAW_FILE_NAME = ''
        self.TARGET_PATH = Path.cwd() / 'data' / 'reference_forms'
        self.EXTRACT_PATH = self.TARGET_PATH / 'CompaniesReferenceForms'
        self.XML_TARGET_PATH = self.TARGET_PATH / 'xml_files'
        self.FINAL_RAW_PATH = self.TARGET_PATH
        self.FINAL_CSV_PATH = self.TARGET_PATH / 'FRE_forms'
        self.FINAL_HDF_PATH = self.TARGET_PATH / 'FRE_forms'
        self.INITIAL_YEAR = datetime.now().year - 10
        self.FINAL_YEAR = datetime.now().year
        self.company_data = None
        self.company_transformed_data = None

        self.__initializer()

    def __initializer(self):
        if not self.check_if_resource_exists(self.FINAL_CSV_PATH):
            try:
                self.create_destination_path(self.TARGET_PATH)
                self.create_destination_path(self.XML_TARGET_PATH)
                self.create_destination_path(self.EXTRACT_PATH)
                self.create_destination_path(self.FINAL_CSV_PATH)
            except FileExistsError:
                pass  # insert log exception
            finally:
                if self.check_download_url(self.ZIP_FILE_URL) < 400:
                    self._get_resource()
                    # self._transform_resource()
                    # self._save_resource()
                else:
                    self.company_transformed_data = pd.read_csv(self.FINAL_CSV_PATH)

    def _get_resource(self):
        zip_files = []
        csv_files = []

        for year in range(self.INITIAL_YEAR, self.FINAL_YEAR):
            zip_files.append(f'fre_cia_aberta_{year}.zip')
            csv_files.append(f'fre_cia_aberta_{year}.csv')

        for file in zip_files:
            self.RAW_FILE_NAME = file
            self.FINAL_RAW_PATH = Path.joinpath(self.TARGET_PATH, self.RAW_FILE_NAME)

            if not self.check_if_resource_exists(self.FINAL_RAW_PATH):
                url = f'{self.ZIP_FILE_URL}{file}'
                wget.download(url, str(self.TARGET_PATH))
                ZipFile(self.FINAL_RAW_PATH, 'r').extract(file.replace('.zip', '.csv'), self.EXTRACT_PATH)
                Path.unlink(self.FINAL_RAW_PATH)

        for file in csv_files:
            print(file)
            self.XML_TARGET_PATH = self.TARGET_PATH / 'xml_files' / file.replace('.csv', '')
            self.create_destination_path(self.XML_TARGET_PATH)
            self.RAW_FILE_NAME = file

            for year in range(self.INITIAL_YEAR, self.FINAL_YEAR):
                self.FINAL_RAW_PATH = Path.joinpath(self.EXTRACT_PATH, self.RAW_FILE_NAME)
                self.company_data = pd.read_csv(self.FINAL_RAW_PATH,
                                                sep=';',
                                                decimal=',',
                                                encoding='ISO-8859-1')
                self.company_data = self.company_data.sort_values('DT_RECEB').groupby('CD_CVM').tail(1)

            url_number = 0
            for url in self.company_data['LINK_DOC'].to_list():
                url_number += 1
                url_length = len(self.company_data['LINK_DOC'].to_list())
                print(f'Reading URL {url_number} of {url_length}')
                response = requests.post(url)
                unzipped = ZipFile(BytesIO(response.content))
                [unzipped.extract(fre, self.XML_TARGET_PATH) for fre in unzipped.namelist() if fre.endswith('.fre')]
                unzipped.close()

    def _transform_resource(self):
        pass

    def _save_resource(self):
        pass
