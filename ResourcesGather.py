from CompanyRegistrationInfoBO import CompanyRegistrationInfoBO
from CompanyFinancialReportsBO import CompanyFinancialReportsBO
from CompanyReferenceFormBO import CompanyReferenceFormBO
from ISINDownloader import ISINDownloader
from InstrumentsFileDownloader import InstrumentsFileDownloader
from TradedInstrumentsBO import TradedInstrumentsBO
from CompanyStockPricesBO import CompanyStockPricesBO


class ResourceGather:
    def __init__(self):
        CompanyRegistrationInfoBO()
        CompanyFinancialReportsBO()
        CompanyReferenceFormBO()
        InstrumentsFileDownloader()
        ISINDownloader()
        TradedInstrumentsBO()
        CompanyStockPricesBO()


if __name__ == '__main__':
    ResourceGather()
