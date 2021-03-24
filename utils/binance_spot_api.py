import hashlib, hmac, http.client, json, requests, time, urllib.parse
from requests.packages.urllib3.util.retry import Retry

from utils.constants import SETTINGS_FILE_NAME
from utils.timeout_http_adapter import TimeoutHTTPAdapter


# BINANCE_SPOT_DEPTH_URL = "https://api.binance.com/api/v1/depth?symbol="
BINANCE_SPOT_DEPTH_URL = "https://testnet.binance.vision/api/v1/depth?symbol="

BINANCE_PRIVATE_API_SPOT_URL = 'https://testnet.binance.vision'  # https://api.binance.com/api   https://testnet.binance.vision/api


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

        return float(glass[0][0]) if glass else None

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

    def place_order(self, price, quantity):
        url = BINANCE_PRIVATE_API_SPOT_URL + '/api/v3/order'
        headers = {'X-MBX-APIKEY': self._api_key}
        data = {
            'symbol': self._currency_pair,
            'side': self._deal_type,
            'type': 'MARKET',
            'quantity': quantity,
        }
        # 'positionSide': 'LONG',
        # 'timeInForce': "GTC",
        # 'price': price,
        payload = self._create_payload(data)

        is_complete = False
        response = None
        while not is_complete:
            # self._logger.info('Попытка поставить позицию ' + str((price, quantity, type)))
            try:
                response = requests.request(method='POST', url=url, params=payload, headers=headers)
                is_complete = True
            except Exception as e:
                # self._logger.error('При запросе к binance произошла ошибка')
                # self._logger.error(e)
                time.sleep(2)
                # self._logger.info('Снова посылаем запрос')

        try:
            result = response.json()
        except Exception as e:
            # self._logger.error('Ошибка в попытке расшифровать json файл', exc_info=True)
            # self._logger.error('response: ', response)
            return str(response)

        return result

    def get_balance(self):
        url = BINANCE_PRIVATE_API_SPOT_URL + '/api/v3/account'
        headers = {'X-MBX-APIKEY': self._api_key}
        payload = self._create_payload({})

        is_complete = False
        response = None
        while not is_complete:
            # self._logger.info('Попытка поставить позицию ' + str((price, quantity, type)))
            try:
                response = requests.request(method='GET', url=url, params=payload, headers=headers)
                is_complete = True
            except Exception as e:
                # self._logger.error('При запросе к binance произошла ошибка')
                # self._logger.error(e)
                time.sleep(2)
                # self._logger.info('Снова посылаем запрос')
        try:
            result = response.json()
        except Exception as e:
            # self._logger.error('Ошибка в попытке расшифровать json файл', exc_info=True)
            # self._logger.error('response: ', response)
            return str(response)

        return result

    def get_trade_list(self):
        url = BINANCE_PRIVATE_API_SPOT_URL + '/api/v3/myTrades'
        headers = {'X-MBX-APIKEY': self._api_key}
        data = {'symbol': self._currency_pair}
        payload = self._create_payload(data)

        is_complete = False
        response = None
        while not is_complete:
            # self._logger.info('Попытка поставить позицию ' + str((price, quantity, type)))
            try:
                response = requests.request(method='GET', url=url, params=payload, headers=headers)
                is_complete = True
            except Exception as e:
                # self._logger.error('При запросе к binance произошла ошибка')
                # self._logger.error(e)
                time.sleep(2)
                # self._logger.info('Снова посылаем запрос')

        try:
            result = response.json()
        except Exception as e:
            # self._logger.error('Ошибка в попытке расшифровать json файл', exc_info=True)
            # self._logger.error('response: ', response)
            return str(response)

        return result

    def get_exchange_info(self):
        url = BINANCE_PRIVATE_API_SPOT_URL + '/api/v3/exchangeInfo'
        headers = {'X-MBX-APIKEY': self._api_key}
        payload = ''

        is_complete = False
        response = None
        while not is_complete:
            # self._logger.info('Попытка поставить позицию ' + str((price, quantity, type)))
            try:
                response = requests.request(method='GET', url=url, params=payload, headers=headers)
                is_complete = True
            except Exception as e:
                # self._logger.error('При запросе к binance произошла ошибка')
                # self._logger.error(e)
                time.sleep(2)
                # self._logger.info('Снова посылаем запрос')

        try:
            result = response.json()
        except Exception as e:
            # self._logger.error('Ошибка в попытке расшифровать json файл', exc_info=True)
            # self._logger.error('response: ', response)
            return str(response)

        return result


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

    obj = BinanceSpotAPI("BUY", "ETHBTC")
    result_of_placement_order = obj.place_order(1500, 0.1)
    print(result_of_placement_order)

    # glass_price = obj.get_binance_price()
    # print(glass_price)

    trade_list = obj.get_trade_list()
    print(trade_list)

    # exchange_info = obj.get_exchange_info()
    # print(exchange_info)
    # import pprint
    # pprint.pprint(exchange_info)

    # balance = obj.get_balance()
    # print(balance)

