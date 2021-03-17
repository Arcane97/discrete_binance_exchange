import json, requests
from requests.packages.urllib3.util.retry import Retry

from utils.constants import SETTINGS_FILE_NAME
from utils.timeout_http_adapter import TimeoutHTTPAdapter


BINANCE_SPOT_DEPTH_URL = "https://api.binance.com/api/v1/depth?symbol="

BINANCE_API_SPOT_URL = 'https://testnet.binance.vision/api'  # https://api.binance.com/api   https://testnet.binance.vision/api


class BinanceSpotAPI:
    def __init__(self, deal_type, currency_pair):

        # тип сделки (покупка или продажа)
        self._deal_type = deal_type
        # валютная пара
        self._currency_pair = currency_pair

        self._api_key = None
        self._api_secret = None

        self._read_api_keys_from_file()

    def _read_api_keys_from_file(self):  # todo подумать над реализвацией сохранения api ключей
        """ Считывание апи ключей из файла
        """
        with open(SETTINGS_FILE_NAME, "r") as file:
            settings_data = json.load(file)
            if isinstance(settings_data, dict):
                self._api_key = settings_data.get('binance_spot_api_key')
                self._api_secret = settings_data.get('binance_spot_api_secret')
            else:
                # error кривой json файл
                pass

    def get_binance_price(self):
        """ Получение цены продажи на бинансе
        :return: цена продажи на бинансе
        """
        try:
            # получаем только 5 ордеров
            limit = '&limit=5'
            # получаем стакан с ордерами на покупку
            query = BINANCE_SPOT_DEPTH_URL + self._currency_pair + limit

            s = requests.Session()
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
                            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"])
            s.mount('http://', TimeoutHTTPAdapter(max_retries=retries))
            s.mount('https://', TimeoutHTTPAdapter(max_retries=retries))

            glass_req = s.get(query)

        except Exception as e:
            # self._logger.error('Ошибка при получении данных из стакана на бинансе')
            # self._logger.error(e)
            return None

        # попытка расшифровать json файл
        try:
            glass_req_result = glass_req.json()
            if self._deal_type == "SELL":
                glass = glass_req_result.get('bids')
            else:
                glass = glass_req_result.get('asks')

        except Exception as e:
            # self._logger.error('Ошибка в попытке расшифровать json файл бинанс')
            # self._logger.error(e)
            return None

        return float(glass[0][0]) if glass is not None else None


if __name__ == "__main__":
    import os

    def create_test_json_file():
        if not os.path.exists(SETTINGS_FILE_NAME):
            with open(SETTINGS_FILE_NAME, "w") as file:
                data = {'binance_spot_api_key': 'sasfasfq231312sasd',
                        'binance_spot_api_secret': 'dasdasdasdasd'}

                json.dump(data, file)
        else:
            with open(SETTINGS_FILE_NAME, "r") as read_file:
                data = json.load(read_file)
                data['binance_spot_api_key'] = 'sasfasfq231312sasd'
                data['binance_spot_api_secret'] = 'dasdasdasdasd'

                with open(SETTINGS_FILE_NAME, "w") as out_file:
                    json.dump(data, out_file)

    # create_test_json_file()

    obj = BinanceSpotAPI("SELL", "BTCUSDT")
    glass = obj.get_binance_price()
    print(glass)

