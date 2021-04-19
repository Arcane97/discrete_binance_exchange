import requests, time
from requests.packages.urllib3.util.retry import Retry

from utils.timeout_http_adapter import TimeoutHTTPAdapter

from utils.binance_base_api import BinanceBaseAPI


# BINANCE_SPOT_API_URL = "https://api.binance.com"
BINANCE_SPOT_API_URL = "https://testnet.binance.vision"

BINANCE_PRIVATE_API_SPOT_URL = 'https://testnet.binance.vision'  # https://api.binance.com/api   https://testnet.binance.vision/api


class BinanceSpotAPI(BinanceBaseAPI):
    def __init__(self, deal_type, currency_pair):
        super().__init__(dict_key_prefix='binance_spot')

        # тип сделки (покупка или продажа)
        self._deal_type = deal_type
        # валютная пара
        self._currency_pair = currency_pair

        self._api_key = None
        self._api_secret = None

        self._read_api_keys_from_file()

    def get_binance_history_per_minute(self):
        """ Получение истории торгов на бинансе за минуту
        :return: история торгов на бинансе за минуту
        """
        try:
            now_time = int(time.time() * 1000)
            time_minute_ago = now_time - 60000
            query = f'{BINANCE_SPOT_API_URL}/api/v1/aggTrades?symbol={self._currency_pair}&startTime={time_minute_ago}&endTime={now_time}&limit=1000'

            s = requests.Session()
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
                            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"])
            s.mount('http://', TimeoutHTTPAdapter(max_retries=retries))
            s.mount('https://', TimeoutHTTPAdapter(max_retries=retries))

            history_req = s.get(query)

        except Exception as e:
            # self._logger.error('Ошибка при получении данных из стакана на бинансе')
            # self._logger.error(e)
            return None

        # попытка расшифровать json файл
        try:
            history_req_result = history_req.json()
            return history_req_result
        except Exception as e:
            # self._logger.error('Ошибка в попытке расшифровать json файл бинанс')
            # self._logger.error(e)
            return None

    def get_average_price_per_minute(self):
        """ Получение средней цены за минуту
        :return: средняя цена за минуту
        """
        history = self.get_binance_history_per_minute()
        if not history:
            return None

        sum_of_all_trades = 0.0
        qty_of_all_trades = 0.0
        for deal in history:
            sum_of_all_trades += float(deal['p']) * float(deal['q'])
            qty_of_all_trades += float(deal['q'])

        return sum_of_all_trades / qty_of_all_trades

    def get_average_price(self):
        """ Получение средней цены за 5 минут
        """
        try:
            query = f'{BINANCE_SPOT_API_URL}/api/v3/avgPrice?symbol={self._currency_pair}'

            s = requests.Session()
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
                            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"])
            s.mount('http://', TimeoutHTTPAdapter(max_retries=retries))
            s.mount('https://', TimeoutHTTPAdapter(max_retries=retries))

            average_price_req = s.get(query)

        except Exception as e:
            # self._logger.error('Ошибка при получении данных из стакана на бинансе')
            # self._logger.error(e)
            return None

        # попытка расшифровать json файл
        try:
            average_price_req_result = average_price_req.json()
            if 'price' in average_price_req_result:
                return average_price_req_result.get('price')

        except Exception as e:
            # self._logger.error('Ошибка в попытке расшифровать json файл бинанс')
            # self._logger.error(e)
            return None
        return None

    def get_binance_glass(self):
        """ Получение стакана на бинансе
        :return: стакан на бинансе
        """
        try:
            # получаем только 5 ордеров
            limit = '&limit=5'
            # получаем стакан с ордерами на покупку
            query = BINANCE_SPOT_API_URL + '/api/v1/depth?symbol=' + self._currency_pair + limit

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

    def place_order(self, quantity):
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

        if 'balances' in result:
            return result['balances']

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
    import json, os
    from utils.constants import SETTINGS_FILE_NAME

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
    result_of_placement_order = obj.place_order(0.1)
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

