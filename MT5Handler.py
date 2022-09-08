from config import MT5Config
import MetaTrader5 as mt5
import pandas as pd
from pathlib import Path


class Mt5Handler:
    # incluir no arquivo de log

    def __init__(self, **kwargs):
        self.MAGIC_NUMBER = 234000
        self.COMMENT = 'StockSelector'
        self.CONFIG = MT5Config()
        self.STARTED_SUCCESSFULLY = self.start_mt5()
        self.ACCOUNT_INFO = self.get_account_info()
        self.TRADED_SYMBOLS = kwargs.get('symbols', None)
        self.DOWNLOAD_PRICES_PATH = Path.cwd() / 'data' / 'prices' / 'individual_prices'
        self.COLECTED_SYMBOLS = []
        self.print_status()
        self.__initializer()

    def __initializer(self):
        try:
            self.DOWNLOAD_PRICES_PATH.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            pass  # insert log exception

    def start_mt5(self):
        return mt5.initialize(login=self.CONFIG.get_user(),
                              server=self.CONFIG.get_server(),
                              password=self.CONFIG.get_pass())

    @staticmethod
    def get_account_info():
        account_info = mt5.account_info()._asdict()
        account_info = pd.DataFrame(list(account_info.items()), columns=['property', 'value'])

        return account_info

    def print_status(self):
        if self.STARTED_SUCCESSFULLY:
            print('Conectado com sucesso.')
            print('Versão: ', mt5.version(), '\n\n')
            print(self.ACCOUNT_INFO, end='\n \n')
        else:
            print('Falha na inicialização. ERRO: ', mt5.last_error())
            quit()

    def get_traded_stocks_daily_prices(self):
        for symbol in self.TRADED_SYMBOLS:
            csv_path = self.DOWNLOAD_PRICES_PATH / f'{symbol}_daily.csv'
            try:
                symbol_prices = pd.DataFrame(mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 99999))
                symbol_prices['datetime'] = pd.to_datetime(symbol_prices['time'], unit='s')
                symbol_prices = symbol_prices[['datetime', 'time', 'open', 'high', 'low',
                                               'close', 'tick_volume', 'spread', 'real_volume']]

                symbol_prices.to_csv(csv_path, index=False)
                print(f'Cotações de {symbol} coletadas.')
                self.COLECTED_SYMBOLS.append(symbol)
            except:
                pass

    @staticmethod
    def finish_mt5():
        mt5.shutdown()
