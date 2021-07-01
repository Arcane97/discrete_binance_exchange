import logging
import requests
import time

from utils.binance_base_api import BinanceBaseAPI
from utils.constants import BINANCE_FUTURES_FILTERS

# BINANCE_FUTURES_API_URL = "https://fapi.binance.com"
BINANCE_FUTURES_API_URL = "https://testnet.binancefuture.com"


class BinanceFuturesAPI(BinanceBaseAPI):
    def __init__(self, deal_type, currency_pair, logger_name="binance_futures_api"):
        super().__init__(dict_key_prefix='binance_futures', logger_name=f'{logger_name}.binance_futures_api')

        # тип сделки (покупка или продажа)  BUY - long, SELL - short
        self._deal_type = deal_type
        # валютная пара
        self._currency_pair = currency_pair

        self._api_key = None
        self._api_secret = None

        self._read_api_keys_from_file()

        self._logger = logging.getLogger(f'{logger_name}.binance_futures_api')

    def get_binance_glass(self):
        """ Получение стакана на бинансе
        :return: стакан на бинансе
        """
        url = f'{BINANCE_FUTURES_API_URL}/fapi/v1/depth?symbol={self._currency_pair}&limit=1000'
        glass_req_result = self._make_get_request(url)

        if not isinstance(glass_req_result, dict):
            return None

        if self._deal_type == "SELL":
            glass = glass_req_result.get('bids')
        else:
            glass = glass_req_result.get('asks')

        return glass if glass else None

    def get_average_price(self):
        """ Получение средней цены
        """
        url = f'{BINANCE_FUTURES_API_URL}/fapi/v1/premiumIndex?symbol={self._currency_pair}'
        average_price_req_result = self._make_get_request(url)

        if not isinstance(average_price_req_result, dict):
            return None

        return float(average_price_req_result.get('markPrice'))

    def get_binance_futures_history(self): # устаревшая функция
        url = 'https://fapi.binance.com/fapi/v1/trades?symbol=' + self._currency_pair
        is_complete = False
        result = None
        while not is_complete:
            try:
                response = requests.get(url)
                is_complete = True
            except Exception:
                self._logger.error('При получении данных из истории binance futures возникла ошибка', exc_info=True)
                continue

            try:
                result = response.json()
            except Exception:
                self._logger.error('Ошибка в попытке расшифровать json файл', exc_info=True)
                time.sleep(2)

        return result

    def get_satisfy_price(self):
        """ Получение удовлетворяющей цены для точной покупки или продажи
        Чтобы ордер сразу совершился
        """
        # множители для ограничения цены сверху и снизу
        multiplier_up = BINANCE_FUTURES_FILTERS[self._currency_pair]['multiplierUp']
        multiplier_down = BINANCE_FUTURES_FILTERS[self._currency_pair]['multiplierDown']
        # получение стакана
        glass = self.get_binance_glass()
        if glass is None:
            return None
        # получение средней цены
        average_price = self.get_average_price()
        if average_price is None:
            return None
        # ограничение цены сверху
        top_limit = average_price * multiplier_up
        # ограничение цены снизу
        bottom_limit = average_price * multiplier_down

        # лямбда функция фильтра: убирает из стакана не удовлетворяющие ордера в интервале цен [bottom_limit, top_limit]
        mapping_percent_price_filter = lambda order: bottom_limit < float(order[0]) < top_limit
        # отфильтрованный стакан
        filtered_glass = list(filter(mapping_percent_price_filter, glass))

        if len(filtered_glass) == 0:
            self._logger.error('Ни один из ордеров в стакане не подходит под фильтр')
            return None
        if len(filtered_glass) == 1:
            return float(filtered_glass[0][0])

        return float(filtered_glass[len(filtered_glass)//2][0])

    def get_price(self, is_buy=True):  # устаревшая функция
        history = self.get_binance_futures_history()
        for deal in reversed(history):
            if deal['isBuyerMaker'] == is_buy:
                return float(deal['price'])

        return history[-1]['price']

    def get_exchange_info(self):
        url = 'https://fapi.binance.com' + '/fapi/v1/exchangeInfo'
        headers = {'X-MBX-APIKEY': self._api_key}
        payload = ''

        is_complete = False
        response = None
        while not is_complete:
            self._logger.info('Попытка получения общей информации')
            try:
                response = requests.request(method='GET', url=url, params=payload, headers=headers)
                is_complete = True
            except Exception:
                self._logger.error('При попытке получения общей информации произошла ошибка', exc_info=True)
                time.sleep(2)
                self._logger.info('Снова посылаем запрос')

        try:
            result = response.json()
        except Exception:
            self._logger.error('Ошибка в попытке расшифровать json файл', exc_info=True)
            self._logger.error(f'Ответ: {response}')
            return str(response)

        return result

    def place_order(self, quantity):
        url = "https://testnet.binancefuture.com/fapi/v1/order"  # todo
        # удовлетворяющая цена
        is_complete = False
        price = None
        while not is_complete:
            price = self.get_satisfy_price()
            is_complete = True if price else False

        headers = {'X-MBX-APIKEY': self._api_key}
        data = {
            'symbol': self._currency_pair,
            'side': self._deal_type,
            'type': 'LIMIT',
            "timeInForce": "GTC",
            'price': price,
            'quantity': quantity,
        }
        payload = self._create_payload(data)

        is_complete = False
        response = None
        while not is_complete:
            self._logger.info(f'Попытка поставить позицию: цена {price}, количество: {quantity}, тип: {self._deal_type}')
            try:
                response = requests.request(method='POST', url=url, params=payload, headers=headers)
                is_complete = True
            except Exception:
                self._logger.error('При запросе к binance произошла ошибка', exc_info=True)
                time.sleep(2)
                self._logger.info('Снова посылаем запрос')

        try:
            result = response.json()
        except Exception:
            self._logger.error('Ошибка в попытке расшифровать json файл', exc_info=True)
            self._logger.error(f'Ответ: {response}')
            return str(response)

        return result


if __name__ == "__main__":
    import json, os
    from utils.constants import SETTINGS_FILE_NAME

    def create_test_json_file():
        if not os.path.exists(SETTINGS_FILE_NAME):
            with open(SETTINGS_FILE_NAME, "w") as file:
                data = {'binance_futures_api_key': 'sasfasfq231312sasd',
                        'binance_futures_api_secret': 'dasdasdasdasd'}

                json.dump(data, file)
        else:
            with open(SETTINGS_FILE_NAME, "r") as read_file:
                data = json.load(read_file)
                data['binance_futures_api_key'] = 'sasfasfq231312sasd'
                data['binance_futures_api_secret'] = 'dasdasdasdasd'

                with open(SETTINGS_FILE_NAME, "w") as out_file:
                    json.dump(data, out_file)

    # create_test_json_file()

    obj = BinanceFuturesAPI("BUY", "BTCUSDT")
    # result = obj.get_binance_glass()
    # print(result)
    import pprint
    # pprint.pprint(result)

    # exchange_info = obj.get_exchange_info().get('symbols')
    # # pprint.pprint(exchange_info)
    # symbols_filters = {pair_info['symbol']: {
    #     'minPrice': pair_info['filters'][0]['tickSize'],  # минимальная цена
    #     'minQty': pair_info['filters'][2]['stepSize'],  # минимальное количество
    #     'multiplierDown': pair_info['filters'][6]['multiplierDown'],
    #     'multiplierUp': pair_info['filters'][6]['multiplierUp'],
    # } for pair_info in exchange_info}
    # pprint.pprint(symbols_filters)

    # average_price = obj.get_average_price()
    # print(average_price, type(average_price))

    # satisfy_price = obj.get_satisfy_price()
    # print(satisfy_price)

