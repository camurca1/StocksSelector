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
        self.company_transformed_data = []
        self.unpack_fre()

    def unpack_fre(self):
        for child_dir in self.FRE_PATH.iterdir():
            fre_files = self.FRE_PATH / child_dir
            for file in fre_files.iterdir():
                self.FINAL_XML_PATH = fre_files / str(file).replace('.fre', '')
                unpacked_fre = ZipFile(file, 'r')
                self.company_data = _CompanyReferenceFormDTO()
                self.company_data.CD_CVM = self._get_company_cvm_code(unpacked_fre)
                self.company_data.REF_DATE = self._get_reference_date(unpacked_fre)
                self.company_data.ACIONISTAS = self._get_stock_holders(unpacked_fre)

                # print(self.company_data.ACIONISTAS)
                break
            break

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

    @staticmethod
    def _get_stock_holders(unpacked_fre):
        stock_holders = unpacked_fre.open('ControleAcionario.xml')
        stock_holders_xml_data = ET.parse(stock_holders)
        stock_holders_xml_root = stock_holders_xml_data.getroot()
        stock_holders_xml_str = ET.tostring(stock_holders_xml_root, encoding='utf-8', method='xml')
        stock_holders_raw = xmltodict.parse(stock_holders_xml_str, process_namespaces=True).pop('ArrayOfControleAcionarioAcionista')

        holders = pd.DataFrame(
            columns=['NumeroIdentificacaoAcionista',
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

        for stock_holder in stock_holders_raw['ControleAcionarioAcionista']:
            new_row = [stock_holder['NumeroIdentificacaoAcionista'],
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


class _CompanyReferenceFormDTO:
    def __init__(self):
        self.CD_CVM = None
        self.REF_DATE = None
        self.ACIONISTAS = None
