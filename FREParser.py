from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd


class FREParser:
    def __init__(self):
        self.FRE_PATH = Path.cwd() / 'data' / 'reference_forms' / 'xml_files'
        self.FINAL_XML_PATH = ''
        self.company_data = None
        self.company_transformed_data = _CompanyReferenceFormDTO()
        self.company_transformed_data.SHARECAPITAL = pd.DataFrame()
        self.company_transformed_data.DIVIDEND_DETAILS = pd.DataFrame()
        self._unpack_fre()

    def _unpack_fre(self):
        for child_dir in self.FRE_PATH.iterdir():
            fre_files = self.FRE_PATH / child_dir
            print(fre_files)
            for file in fre_files.iterdir():
                print(file)
                self.FINAL_XML_PATH = fre_files / str(file).replace('.fre', '')
                unpacked_fre = ZipFile(file, 'r')
                self.company_data = _CompanyReferenceFormDTO()
                self.company_data.CD_CVM = self._get_company_cvm_code(unpacked_fre)
                self.company_data.REF_DATE = self._get_reference_date(unpacked_fre)
                self.company_data.SHAREHOLDERS = self._get_stock_holders(unpacked_fre)
                self.company_data.SHARECAPITAL = self._get_share_capital(unpacked_fre)
                self.company_data.DIVIDEND_DETAILS = self._get_dividend_details(unpacked_fre)

                if not self.company_data.SHARECAPITAL is None:
                    if len(self.company_data.SHARECAPITAL):
                        self.company_transformed_data.SHARECAPITAL = pd.concat([self.company_transformed_data.SHARECAPITAL,
                                                                                self.company_data.SHARECAPITAL])

                if not self.company_data.DIVIDEND_DETAILS is None:
                    if len(self.company_data.DIVIDEND_DETAILS):
                        self.company_transformed_data.DIVIDEND_DETAILS = pd.concat([self.company_transformed_data.DIVIDEND_DETAILS,
                                                                                    self.company_data.DIVIDEND_DETAILS])

    @staticmethod
    def _get_company_cvm_code(unpacked_fre):
        fre = unpacked_fre.open('FormularioReferencia.xml')
        fre = pd.read_xml(fre, xpath='//CompanhiaAberta',
                          namespaces={'FormularioReferencia': 'http://www.w3.org/2001/XMLSchema'})
        return fre['CodigoCvm'].to_list()[0]

    @staticmethod
    def _get_reference_date(unpacked_fre):
        fre = unpacked_fre.open('FormularioReferencia.xml')
        fre = pd.read_xml(fre, xpath='//Documento',
                          namespaces={'FormularioReferencia': 'http://www.w3.org/2001/XMLSchema'})
        return fre['DataReferenciaDocumento'].to_list()[0]

    def _get_stock_holders(self, unpacked_fre):
        xml = unpacked_fre.open('ControleAcionario.xml')
        xml_data = ET.parse(xml)
        xml_root = xml_data.getroot()
        xml_str = ET.tostring(xml_root, encoding='utf-8', method='xml')
        dict_raw = xmltodict.parse(xml_str, process_namespaces=True).pop('ArrayOfControleAcionarioAcionista')

        holders = pd.DataFrame(
            columns=['CD_CVM',
                     'DT_REFER',
                     'NumeroIdentificacaoAcionista',
                     'TipoRegistro',
                     'NumeroPessoa',
                     'IdentificacaoPessoa',
                     'NomePessoa',
                     'TipoPessoa',
                     'Nacionalidade',
                     'CodigoEstado',
                     'SiglaEstado',
                     'NomeEstado',
                     'QuantidadeAcoesOrdinarias',
                     'PercentualAcoesOrdinarias',
                     'QuantidadeAcoesPreferenciais',
                     'PercentualAcoesPreferenciais',
                     'QuantidadeTotalAcoes',
                     'PercentualTotalAcoes',
                     'ParticipanteAcionista',
                     'AcionistaControlador'])

        for stock_holder in dict_raw['ControleAcionarioAcionista']:
            new_row = [self.company_data.CD_CVM,
                       self.company_data.REF_DATE,
                       stock_holder['NumeroIdentificacaoAcionista'],
                       stock_holder['TipoRegistro'],
                       stock_holder['Pessoa']['NumeroPessoa'],
                       stock_holder['Pessoa']['IdentificacaoPessoa'],
                       stock_holder['Pessoa']['NomePessoa'],
                       stock_holder['Pessoa']['TipoPessoa'],
                       stock_holder['Nacionalidade'],
                       stock_holder['Estado']['CodigoEstado'],
                       stock_holder['Estado']['SiglaEstado'],
                       stock_holder['Estado']['NomeEstado'],
                       stock_holder['QuantidadeAcoesOrdinarias'],
                       stock_holder['PercentualAcoesOrdinarias'],
                       stock_holder['QuantidadeAcoesPreferenciais'],
                       stock_holder['PercentualAcoesPreferenciais'],
                       stock_holder['QuantidadeTotalAcoes'],
                       stock_holder['PercentualTotalAcoes'],
                       True if stock_holder['ParticipanteAcionista'] == 1 else False,
                       True if stock_holder['AcionistaControlador'] == 1 else False]

            holders.loc[len(holders)] = new_row

        return holders

    def _get_share_capital(self, unpacked_fre):
        xml = unpacked_fre.open('CapitalSocial.xml')
        dict_raw = self._xml_to_dict(xml, 'ArrayOfCapitalSocial')

        capital = self._create_dataframe(['CD_CVM',
                                          'DT_REFER',
                                          'CodigoTipoCapital',
                                          'DataAutorizacaoCapital',
                                          'ValorCapitalSocial',
                                          'PrazoIntegralizado',
                                          'QuantidadeAcoesOrdinarias',
                                          'QuantidadeAcoesPreferenciais',
                                          'QuantidadeTotalAcoes',
                                          'TitulosConversaoAcao'])

        if not dict_raw is None:
            for share_capital in dict_raw['CapitalSocial']:
                try:
                    if self._decode_share_capital_type(share_capital['CodigoTipoCapital']) == 'Capital Integralizado':
                        new_row = [self.company_data.CD_CVM,
                                   self.company_data.REF_DATE,
                                   self._decode_share_capital_type(share_capital['CodigoTipoCapital']),
                                   share_capital['DataAutorizacaoCapital'],
                                   share_capital['ValorCapitalSocial'],
                                   share_capital['PrazoIntegralizado'],
                                   share_capital['QuantidadeAcoesOrdinarias'],
                                   share_capital['QuantidadeAcoesPreferenciais'],
                                   share_capital['QuantidadeTotalAcoes'],
                                   share_capital['TitulosConversaoAcao']]

                        capital.loc[len(capital)] = new_row

                except Exception:
                    pass

            return capital

    @staticmethod
    def _decode_share_capital_type(code):
        if code == '1':
            return 'Capital Emitido'
        if code == '2':
            return 'Capital Subscrito'
        if code == '3':
            return 'Capital Integralizado'
        if code == '4':
            return 'Capital Autorizado'

    def _get_dividend_details(self, unpacked_fre):
        xml = unpacked_fre.open('InformacoesFinanceirasSelecionadas.xml')
        dict_raw = self._xml_to_dict(xml, 'ArrayOfInfoFinSel')

        dividend_details = self._create_dataframe(['CD_CVM',
                                                   'DT_REFER',
                                                   'DataInicioExercicioSocial',
                                                   'DataFimExercicioSocial',
                                                   'LucroLiquido',
                                                   'DividendoDistribuido',
                                                   'LucroLiquidoRetido',
                                                   'TaxaRetorno',
                                                   'PercentualDividendoDistribuido',
                                                   'DataAprovacaoRetencao'])

        if not dict_raw is None:
            for dividend in dict_raw['InfoFinSel']:
                try:
                    new_row = [self.company_data.CD_CVM,
                               self.company_data.REF_DATE,
                               dividend['ExercicioSocial']['DataInicioExercicioSocial'],
                               dividend['ExercicioSocial']['DataFimExercicioSocial'],
                               dividend['LucroLiquido'],
                               dividend['DividendoDistribuido'],
                               dividend['LucroLiquidoRetido'],
                               dividend['TaxaRetorno'],
                               dividend['PercentualDividendoDistribuido'],
                               dividend['DataAprovacaoRetencao']]

                    dividend_details.loc[0] = new_row

                except Exception:
                    pass

            return dividend_details

    @staticmethod
    def _xml_to_dict(xml, pop_level):
        xml_data = ET.parse(xml)
        xml_root = xml_data.getroot()
        xml_str = ET.tostring(xml_root, encoding='utf-8', method='xml')
        dict_raw = xmltodict.parse(xml_str, process_namespaces=True).pop(pop_level)

        return dict_raw

    @staticmethod
    def _create_dataframe(columns):
        return pd.DataFrame(columns=columns)


class _CompanyReferenceFormDTO:
    def __init__(self):
        self.CD_CVM = None
        self.REF_DATE = None
        self.SHAREHOLDERS = None
        self.SHARECAPITAL = None
        self.DIVIDEND_DETAILS = None
