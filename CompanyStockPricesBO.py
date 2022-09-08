########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 2022-08-24                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: ETL dos preços diários das companhias monitoradas                                                            #
########################################################################################################################
from BaseBO import BaseBO
from pathlib import Path
from datetime import datetime
import pandas as pd
from MT5Handler import Mt5Handler


class CompanyStockPricesBO(BaseBO):
    def __init__(self):
        super(BaseBO, self).__init__()
        self.DATE = datetime.today().strftime('%Y%m%d')
        self.ACTIVE_TRADED_COMPANIES = Path.cwd() / 'data' / 'traded_instruments' / 'active_traded_stocks.csv'
        self.TARGET_PATH = Path.cwd() / 'data' / 'prices'
        self.INDIVIDUAL_PRICES_PATH = self.TARGET_PATH / 'individual_prices'
        self.FINAL_CSV_PATH = self.TARGET_PATH / 'stocks_prices.csv'
        self.company_data = pd.read_csv(self.ACTIVE_TRADED_COMPANIES)
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
        mt5_handler = Mt5Handler(symbols=self.company_data['TckrSymb'].to_list())
        mt5_handler.get_traded_stocks_daily_prices()
        mt5_handler.finish_mt5()

    def _transform_resource(self):
        prices = pd.DataFrame()

        for symbol in self.company_data['TckrSymb'].to_list():
            price_path = self.INDIVIDUAL_PRICES_PATH / f'{symbol}_daily.csv'
            try:
                price = pd.read_csv(price_path,
                                    parse_dates=True,
                                    infer_datetime_format=True)
                price['TckrSymb'] = symbol
                prices = pd.concat([prices, price])
            except:
                print(f'{symbol} não encontrado.')

        prices['datetime'] = pd.to_datetime(prices['datetime'])
        prices.rename(columns={'datetime': 'DT_REFER'}, inplace=True)
        prices.set_index(['DT_REFER', 'TckrSymb'], inplace=True)
        prices.sort_index(inplace=True)
        self.company_transformed_data = prices

    def _save_resource(self):
        self.company_transformed_data.to_csv(self.FINAL_CSV_PATH)
