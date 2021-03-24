import hashlib
import hmac
import json
import time
import urllib.parse

from utils.constants import SETTINGS_FILE_NAME


class BinanceBaseAPI:
    def __init__(self, dict_key_prefix='binance'):
        self._api_key = None
        self._api_secret = None

        self._dict_key_prefix = dict_key_prefix

    def _read_api_keys_from_file(self):  # todo подумать над реализвацией сохранения api ключей
        """ Считывание апи ключей из файла
        """
        with open(SETTINGS_FILE_NAME, "r") as file:
            settings_data = json.load(file)
            if isinstance(settings_data, dict):
                self._api_key = settings_data.get(self._dict_key_prefix + '_api_key')
                self._api_secret = settings_data.get(self._dict_key_prefix + '_api_secret')
            else:
                # error кривой json файл
                pass

    def _create_payload(self, data: dict):
        """ Создание тела запроса
        :return тело запроса в URL (str)
        """
        # создание Timing security
        timestamp = int(round(time.time() * 1000) - 300)
        data['timestamp'] = timestamp
        data['recvWindow'] = 10000

        # создание sha256 подписи
        payload = urllib.parse.urlencode(data)
        api_secret = str.encode(self._api_secret)
        secret_hash = hmac.new(key=api_secret, digestmod=hashlib.sha256)
        secret_hash.update(payload.encode('utf-8'))
        sign = secret_hash.hexdigest()

        # добавление подписи в тело запроса
        data['signature'] = sign

        # парсинг словаря в строку тела url запроса
        return urllib.parse.urlencode(data)
