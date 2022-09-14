########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 2022-09-11                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: Calcular a quantidade total de ações por empresa                                                             #
########################################################################################################################
from BaseBO import BaseBO
from pathlib import Path
import pandas as pd


class TotalCompanySharesBO(BaseBO):
    def __init__(self):
        super(BaseBO, self).__init__()
        self.COMPANIES_TOTAL_SHARES = Path.cwd() / 'data' / 'reference_forms' / 'FRE_forms' / 'companies_fre_2012_2022.csv'
        self.TARGET_PATH = Path.cwd() / 'data' / 'reference_forms'
        self.FINAL_CSV_PATH = self.TARGET_PATH / 'total_shares.csv'
        self.FINAL_JSON_PATH = self.TARGET_PATH / 'total_shares.json'
        self.company_data = None
        self.company_transformed_data = None

        self.__initializer()

    def __initializer(self):
        try:
            self.create_destination_path(self.TARGET_PATH)
        except FileExistsError:
            pass  # insert log exception
        finally:
            self._get_resource()
            self._transform_resource()
            self._save_resource()

    def _get_resource(self):
        self.company_data = pd.read_csv(self.COMPANIES_TOTAL_SHARES, parse_dates=True)

    def _transform_resource(self):
        self.company_transformed_data = self.company_data
        self.company_transformed_data = self.company_transformed_data.groupby(['CD_CVM', 'DT_REFER'], as_index=False)['QuantidadeTotalAcoes'].sum()
        self.company_transformed_data = self.company_transformed_data.reset_index(drop=True).rename(columns={'QuantidadeTotalAcoes': 'total_annual_shares'})

    def _save_resource(self):
        self.company_transformed_data.to_csv(self.FINAL_CSV_PATH, index=False)
        self.company_transformed_data.to_json(self.FINAL_JSON_PATH, orient='records')
