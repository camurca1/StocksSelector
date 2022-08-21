########################################################################################################################
# Criado por: Alexandre Camurça                                                                                        #
# Data: 2022-08-20                                                                                                     #
# Repositório: https://github.com/camurca1/StocksSelector                                                              #
# Função: Classe abstrata utilizada pelos ETL                                                                          #
########################################################################################################################
from abc import ABC, abstractmethod
from pathlib import Path
from requests import head


class BaseBO(ABC):

    @classmethod
    def check_if_resource_exists(cls, path):
        return Path(path).exists()

    @classmethod
    def create_destination_path(cls, path_obj):
        path_obj.mkdir(parents=True, exist_ok=False)

    @classmethod
    def check_download_url(cls, url):
        response = head(url)
        return response.status_code

    @abstractmethod
    def _get_resource(self):
        raise NotImplementedError

    @abstractmethod
    def _transform_resource(self):
        raise NotImplementedError

    @abstractmethod
    def _save_resource(self):
        raise NotImplementedError
