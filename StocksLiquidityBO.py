########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 2022-09-08                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: Calcular a liquidez anual dos ativos                                                                         #
########################################################################################################################
from BaseBO import BaseBO
from pathlib import Path
from datetime import datetime
import pandas as pd


class StocksLiquidityBO(BaseBO):
    def __init__(self):
        super(BaseBO, self).__init__()
        self.DATE = datetime.today().strftime('%Y-%m-%d')
        self.ACTIVE_STOCKS_PRICES = Path.cwd() / 'data' / 'prices' / 'stocks_prices.csv'
        self.TARGET_PATH = Path.cwd() / 'data' / 'prices'
        self.FINAL_CSV_PATH = self.TARGET_PATH / 'liquid_stocks.csv'
        self.FINAL_JSON_PATH = self.TARGET_PATH / 'liquid_stocks.json'
        self.company_data = pd.read_csv(self.ACTIVE_STOCKS_PRICES, parse_dates=True, index_col=['TckrSymb', 'DT_REFER'])
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
        self.company_data = self.company_data.xs(pd.IndexSlice['2015-01-01':self.DATE],
                                                 level='DT_REFER',
                                                 drop_level=False)
        self.company_data.sort_index(inplace=True)

    def _transform_resource(self):
        self.company_transformed_data = self.company_data
        self.company_transformed_data = self.company_transformed_data.reset_index()
        self.company_transformed_data['year'] = self.company_transformed_data['DT_REFER'].dt.year
        self.company_transformed_data['average_traded_volume'] = self.company_transformed_data['close'] * self.company_transformed_data['real_volume']
        self.company_transformed_data = self.company_transformed_data.groupby(['TckrSymb', 'year'], as_index=False)['average_traded_volume'].mean()
        self.company_transformed_data = self.company_transformed_data.reset_index(drop=True).rename(columns={'average_traded_volume': 'average_year_traded_volume'})
        self.company_transformed_data = self.company_transformed_data[self.company_transformed_data.average_year_traded_volume > 1]
        self.company_transformed_data.reset_index(drop=True, inplace=True)
        self.company_transformed_data['year'] = self.company_transformed_data['year'].astype(str) + '-12-31'
        self.company_transformed_data = self.company_transformed_data.rename(columns={'year': 'DT_REFER'})

    def _save_resource(self):
        self.company_transformed_data.to_csv(self.FINAL_CSV_PATH, index=False)
        self.company_transformed_data.to_json(self.FINAL_JSON_PATH, orient='records')
