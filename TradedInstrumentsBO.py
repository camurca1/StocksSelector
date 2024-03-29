########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 2022-08-24                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: ETL dos instrumentos negociados na B3                                                                        #
########################################################################################################################
from B3DateValidator import B3DateValidator
from BaseBO import BaseBO
from pathlib import Path
from datetime import datetime
import pandas as pd
from zipfile import ZipFile
from numpy import r_
from numpy import nan
from DatabaseHandler import DatabaseHandler


class TradedInstrumentsBO(BaseBO):
    def __init__(self):
        super(BaseBO, self).__init__()
        self.DATE = self._get_valid_trade_date(
            datetime.today().strftime('%Y%m%d'))
        self.TARGET_PATH = Path.cwd() / 'data' / 'traded_instruments'
        self.ISIN_ZIP_PATH = self.TARGET_PATH / 'isinp.zip'
        self.CONSOLIDATED_FILE_PATH = self.TARGET_PATH / 'InstrumentsConsolidated' / \
            f'InstrumentsConsolidatedFile_{self.DATE}_1.csv'
        self.COMPANIES_INFO = Path.cwd() / 'data' / 'companies' / \
            'RegularCompaniesRegistrationInfo.csv'
        self.FINAL_CSV_PATH = self.TARGET_PATH / 'active_traded_stocks.csv'

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
            self._connectDB()
            self._save_resource()
            self._disconnectDB()

    @staticmethod
    def _get_valid_trade_date(date):
        market_day = B3DateValidator(date).valid_date.strftime('%Y%m%d')
        return market_day

    @staticmethod
    def _clean_data(df):
        return df.fillna('').astype(str).str.replace('.0', '', regex=False)

    def _connectDB(self):
        self.db = DatabaseHandler()
        self.db.connect()

    def _disconnectDB(self):
        self.db.disconnect()

    def _get_resource(self):
        self.company_data = _IsinDTO()
        unpacked_isin = ZipFile(self.ISIN_ZIP_PATH, 'r')
        self.company_data.EMITTERS = pd.read_csv(unpacked_isin.open('EMISSOR.TXT'),
                                                 sep=',',
                                                 header=None,
                                                 engine='python')
        self.company_data.INSTRUMENTS = pd.read_csv(unpacked_isin.open('NUMERACA.TXT'),
                                                    sep=',',
                                                    header=None,
                                                    engine='python')
        self.company_data.CONSOLIDATED_FILE = pd.read_csv(self.CONSOLIDATED_FILE_PATH,
                                                          sep=';',
                                                          encoding='WINDOWS-1252',
                                                          low_memory=False)
        unpacked_isin.close()

    def _transform_resource(self):
        self.company_data.EMITTERS = pd.DataFrame(self.company_data.EMITTERS.values[:, 0:3],
                                                  columns=['cod_emissor', 'emissor', 'CNPJ'])
        self.company_data.EMITTERS['cod_emissor'] = self.company_data.EMITTERS['cod_emissor'].astype(
            str)
        self.company_data.EMITTERS['CNPJ_CIA'] = self.company_data.EMITTERS['CNPJ'].astype(str).str.replace('.0', '',
                                                                                                            regex=False)
        self.company_data.EMITTERS['CNPJ_CIA'] = self.company_data.EMITTERS['CNPJ_CIA'].str.zfill(
            14)

        self.company_data.INSTRUMENTS = self.company_data.INSTRUMENTS.iloc[:, r_[
            2:6, 20]]
        self.company_data.INSTRUMENTS = pd.DataFrame(self.company_data.INSTRUMENTS.values[:, :],
                                                     columns=['ISIN', 'cod_emissor', 'prefix_emissor', 'desc_ativo',
                                                              'tipo_ativo'])
        self.company_data.INSTRUMENTS = self.company_data.INSTRUMENTS[
            self.company_data.INSTRUMENTS['tipo_ativo'] == 'ACN']
        self.company_data.INSTRUMENTS['cod_emissor'] = self.company_data.INSTRUMENTS['cod_emissor'].astype(
            str)

        self.company_data.NEGOTIATED = pd.read_csv(self.CONSOLIDATED_FILE_PATH,
                                                   sep=';',
                                                   header=1,
                                                   encoding='WINDOWS-1252',
                                                   low_memory=False)
        column_headers = self.company_data.NEGOTIATED.columns.values.tolist()
        print("The Column Header :", column_headers)
        manter_colunas = ['TckrSymb', 'Asst', 'SgmtNm', 'MktNm', 'SctyCtgyNm', 'ISIN', 'SpcfctnCd', 'CrpnNm',
                          'CorpGovnLvlNm']
        self.company_data.NEGOTIATED = self.company_data.NEGOTIATED[
            self.company_data.NEGOTIATED['SctyCtgyNm'] == 'SHARES']
        self.company_data.NEGOTIATED = self.company_data.NEGOTIATED[manter_colunas]

        self.company_data.CIA_ABERTA = pd.read_csv(self.COMPANIES_INFO)

        # print(self.company_data.CIA_ABERTA['DT_REG'].head())
        self.company_data.CIA_ABERTA['CNPJ_CIA'] = self.company_data.CIA_ABERTA['CNPJ_CIA'].astype(
            str)
        self.company_data.CIA_ABERTA['CNPJ_AUDITOR'] = self.company_data.CIA_ABERTA['CNPJ_AUDITOR'].astype(
            str)
        self.company_data.CIA_ABERTA['CEP'] = self._clean_data(
            self.company_data.CIA_ABERTA['CEP'])
        self.company_data.CIA_ABERTA['DDD_TEL'] = self._clean_data(
            self.company_data.CIA_ABERTA['DDD_TEL'])
        self.company_data.CIA_ABERTA['TEL'] = self._clean_data(
            self.company_data.CIA_ABERTA['TEL'])
        self.company_data.CIA_ABERTA['DDD_FAX'] = self._clean_data(
            self.company_data.CIA_ABERTA['DDD_FAX'])
        self.company_data.CIA_ABERTA['FAX'] = self._clean_data(
            self.company_data.CIA_ABERTA['FAX'])
        self.company_data.CIA_ABERTA['CEP_RESP'] = self._clean_data(
            self.company_data.CIA_ABERTA['CEP_RESP'])
        self.company_data.CIA_ABERTA['DDD_TEL_RESP'] = self._clean_data(
            self.company_data.CIA_ABERTA['DDD_TEL_RESP'])
        self.company_data.CIA_ABERTA['TEL_RESP'] = self._clean_data(
            self.company_data.CIA_ABERTA['TEL_RESP'])
        self.company_data.CIA_ABERTA['DDD_FAX_RESP'] = self._clean_data(
            self.company_data.CIA_ABERTA['DDD_FAX_RESP'])
        self.company_data.CIA_ABERTA['FAX_RESP'] = self._clean_data(
            self.company_data.CIA_ABERTA['FAX_RESP'])

        self.company_transformed_data = pd.merge(self.company_data.INSTRUMENTS,
                                                 self.company_data.EMITTERS,
                                                 on=['cod_emissor']).drop_duplicates().drop(['CNPJ'], axis=1)
        self.company_transformed_data = pd.merge(self.company_data.NEGOTIATED, self.company_transformed_data,
                                                 on=['ISIN']).drop_duplicates()
        self.company_transformed_data = pd.merge(
            self.company_transformed_data, self.company_data.CIA_ABERTA, on=['CNPJ_CIA']).drop_duplicates()

    def _save_resource(self):
        self.company_transformed_data.to_csv(
            self.FINAL_CSV_PATH, na_rep='', date_format='%Y-%m-%d', encoding='WINDOWS-1252', index=False)
        self.db.write_active_stocks(self.company_transformed_data)


class _IsinDTO:
    def __init__(self):
        self.EMITTERS = None
        self.INSTRUMENTS = None
        self.NEGOTIATED = None
        self.CIA_ABERTA = None
