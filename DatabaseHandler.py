########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 09/09/2023                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: Interface de manipulação do BD Postgres                                                                      #
########################################################################################################################
import psycopg2
from configparser import ConfigParser


class DatabaseHandler:
    def __init__(self):
        self.CONFIG_FILE = 'database.ini'
        self.CONFIG_FILE_SECTION = 'postgresql'
        self.PARSER = ConfigParser()
        self.DB_PARAMS = self._config()
        self.conn = None
        self.cursor = None

    def _config(self):
        self.PARSER.read(self.CONFIG_FILE)

        database_params = {}

        if self.PARSER.has_section(self.CONFIG_FILE_SECTION):
            params = self.PARSER.items(self.CONFIG_FILE_SECTION)

            for param in params:
                database_params[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file',
                            self.CONFIG_FILE_SECTION, self.CONFIG_FILE)

        return database_params

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.DB_PARAMS)
            self.cursor = self.conn.cursor()
            db_version = self.cursor.fetchone()
            print(db_version)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                print('Database connection established.')

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def write_stocks_prices(self, prices):
        rows = zip(prices.DT_REFER, prices.TckrSymb, prices.time,
                   prices.open, prices.high, prices.low, prices.close,
                   prices.tick_volume, prices.spread, prices.real_volume)

        self.cursor.executemany("""
                                INSERT INTO public."stocksPrices" ("DT_REFER", "TckrSymb", time, open, high, low, close, tick_volume, spread, real_volume)
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT ON CONSTRAINT unique_ts_stock
                                DO NOTHING;""", rows)

        print(
            f'Serão escritas {self.cursor.rowcount} linhas no banco de dados.')
        self.conn.commit()

    def write_active_stocks(self, active_stocks):
        active_stocks = active_stocks.fillna(psycopg2.extensions.AsIs('NULL'))

        rows = zip(active_stocks.TckrSymb, active_stocks.Asst, active_stocks.SgmtNm, active_stocks.MktNm, active_stocks.SctyCtgyNm, active_stocks.ISIN, active_stocks.SpcfctnCd, active_stocks.CrpnNm, active_stocks.CorpGovnLvlNm, active_stocks.cod_emissor, active_stocks.prefix_emissor, active_stocks.desc_ativo, active_stocks.tipo_ativo, active_stocks.emissor, active_stocks.CNPJ_CIA, active_stocks.DENOM_SOCIAL, active_stocks.DENOM_COMERC, active_stocks.DT_REG, active_stocks.DT_CONST, active_stocks.DT_CANCEL, active_stocks.MOTIVO_CANCEL, active_stocks.SIT, active_stocks.DT_INI_SIT, active_stocks.CD_CVM, active_stocks.SETOR_ATIV, active_stocks.TP_MERC, active_stocks.CATEG_REG, active_stocks.DT_INI_CATEG, active_stocks.SIT_EMISSOR, active_stocks.DT_INI_SIT_EMISSOR,
                   active_stocks.CONTROLE_ACIONARIO, active_stocks.TP_ENDER, active_stocks.LOGRADOURO, active_stocks.COMPL, active_stocks.BAIRRO, active_stocks.MUN, active_stocks.UF, active_stocks.PAIS, active_stocks.CEP, active_stocks.DDD_TEL, active_stocks.TEL, active_stocks.DDD_FAX, active_stocks.FAX, active_stocks.EMAIL, active_stocks.TP_RESP, active_stocks.RESP, active_stocks.DT_INI_RESP, active_stocks.LOGRADOURO_RESP, active_stocks.COMPL_RESP, active_stocks.BAIRRO_RESP, active_stocks.MUN_RESP, active_stocks.UF_RESP, active_stocks.PAIS_RESP, active_stocks.CEP_RESP, active_stocks.DDD_TEL_RESP, active_stocks.TEL_RESP, active_stocks.DDD_FAX_RESP, active_stocks.FAX_RESP, active_stocks.EMAIL_RESP, active_stocks.CNPJ_AUDITOR, active_stocks.AUDITOR)

        self.cursor.executemany("""INSERT INTO public."activeStocks" ("TckrSymb","Asst","SgmtNm","MktNm","SctyCtgyNm","ISIN","SpcfctnCd","CrpnNm","CorpGovnLvlNm","cod_emissor","prefix_emissor","desc_ativo","tipo_ativo","emissor","CNPJ_CIA","DENOM_SOCIAL","DENOM_COMERC","DT_REG","DT_CONST","DT_CANCEL","MOTIVO_CANCEL","SIT","DT_INI_SIT","CD_CVM","SETOR_ATIV","TP_MERC","CATEG_REG","DT_INI_CATEG","SIT_EMISSOR","DT_INI_SIT_EMISSOR","CONTROLE_ACIONARIO","TP_ENDER","LOGRADOURO","COMPL","BAIRRO","MUN","UF","PAIS","CEP","DDD_TEL","TEL","DDD_FAX","FAX","EMAIL","TP_RESP","RESP","DT_INI_RESP","LOGRADOURO_RESP","COMPL_RESP","BAIRRO_RESP","MUN_RESP","UF_RESP","PAIS_RESP","CEP_RESP","DDD_TEL_RESP","TEL_RESP","DDD_FAX_RESP","FAX_RESP","EMAIL_RESP","CNPJ_AUDITOR","AUDITOR")
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                ON CONFLICT ("TckrSymb") DO UPDATE
                                SET "TckrSymb" = EXCLUDED."TckrSymb","Asst" = EXCLUDED."Asst","SgmtNm" = EXCLUDED."SgmtNm","MktNm" = EXCLUDED."MktNm","SctyCtgyNm" = EXCLUDED."SctyCtgyNm","ISIN" = EXCLUDED."ISIN","SpcfctnCd" = EXCLUDED."SpcfctnCd","CrpnNm" = EXCLUDED."CrpnNm","CorpGovnLvlNm" = EXCLUDED."CorpGovnLvlNm","cod_emissor" = EXCLUDED."cod_emissor","prefix_emissor" = EXCLUDED."prefix_emissor","desc_ativo" = EXCLUDED."desc_ativo","tipo_ativo" = EXCLUDED."tipo_ativo","emissor" = EXCLUDED."emissor","CNPJ_CIA" = EXCLUDED."CNPJ_CIA","DENOM_SOCIAL" = EXCLUDED."DENOM_SOCIAL","DENOM_COMERC" = EXCLUDED."DENOM_COMERC","DT_REG" = EXCLUDED."DT_REG","DT_CONST" = EXCLUDED."DT_CONST","DT_CANCEL" = EXCLUDED."DT_CANCEL","MOTIVO_CANCEL" = EXCLUDED."MOTIVO_CANCEL","SIT" = EXCLUDED."SIT","DT_INI_SIT" = EXCLUDED."DT_INI_SIT","CD_CVM" = EXCLUDED."CD_CVM","SETOR_ATIV" = EXCLUDED."SETOR_ATIV","TP_MERC" = EXCLUDED."TP_MERC","CATEG_REG" = EXCLUDED."CATEG_REG","DT_INI_CATEG" = EXCLUDED."DT_INI_CATEG","SIT_EMISSOR" = EXCLUDED."SIT_EMISSOR","DT_INI_SIT_EMISSOR" = EXCLUDED."DT_INI_SIT_EMISSOR","CONTROLE_ACIONARIO" = EXCLUDED."CONTROLE_ACIONARIO","TP_ENDER" = EXCLUDED."TP_ENDER","LOGRADOURO" = EXCLUDED."LOGRADOURO","COMPL" = EXCLUDED."COMPL","BAIRRO" = EXCLUDED."BAIRRO","MUN" = EXCLUDED."MUN","UF" = EXCLUDED."UF","PAIS" = EXCLUDED."PAIS","CEP" = EXCLUDED."CEP","DDD_TEL" = EXCLUDED."DDD_TEL","TEL" = EXCLUDED."TEL","DDD_FAX" = EXCLUDED."DDD_FAX","FAX" = EXCLUDED."FAX","EMAIL" = EXCLUDED."EMAIL","TP_RESP" = EXCLUDED."TP_RESP","RESP" = EXCLUDED."RESP","DT_INI_RESP" = EXCLUDED."DT_INI_RESP","LOGRADOURO_RESP" = EXCLUDED."LOGRADOURO_RESP","COMPL_RESP" = EXCLUDED."COMPL_RESP","BAIRRO_RESP" = EXCLUDED."BAIRRO_RESP","MUN_RESP" = EXCLUDED."MUN_RESP","UF_RESP" = EXCLUDED."UF_RESP","PAIS_RESP" = EXCLUDED."PAIS_RESP","CEP_RESP" = EXCLUDED."CEP_RESP","DDD_TEL_RESP" = EXCLUDED."DDD_TEL_RESP","TEL_RESP" = EXCLUDED."TEL_RESP","DDD_FAX_RESP" = EXCLUDED."DDD_FAX_RESP","FAX_RESP" = EXCLUDED."FAX_RESP","EMAIL_RESP" = EXCLUDED."EMAIL_RESP","CNPJ_AUDITOR" = EXCLUDED."CNPJ_AUDITOR","AUDITOR" = EXCLUDED."AUDITOR"
                                """, rows)

        print(
            f'Serão escritas {self.cursor.rowcount} linhas no banco de dados.')
        self.conn.commit()


if __name__ == '__main__':
    db = DatabaseHandler()
    db.connect()
    db.disconnect()
