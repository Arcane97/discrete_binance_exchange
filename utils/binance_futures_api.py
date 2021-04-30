import requests, time

from utils.binance_base_api import BinanceBaseAPI


BINANCE_FUTURES_API_URL = "https://fapi.binance.com"
# BINANCE_FUTURES_API_URL = "https://testnet.binancefuture.com"


class BinanceFuturesAPI(BinanceBaseAPI):
    def __init__(self, deal_type, currency_pair):
        super().__init__(dict_key_prefix='binance_futures')

        # тип сделки (покупка или продажа)
        self._deal_type = deal_type
        # валютная пара
        self._currency_pair = currency_pair

        self._api_key = None
        self._api_secret = None

        self._read_api_keys_from_file()

    def get_binance_glass(self):
        """ Получение стакана на бинансе
        :return: стакан на бинансе
        """
        url = BINANCE_FUTURES_API_URL + '/fapi/v1/depth?symbol=' + self._currency_pair + '&limit=1000'
        glass_req_result = self._make_get_request(url)

        if not isinstance(glass_req_result, dict):
            return None

        if self._deal_type == "SELL":
            glass = glass_req_result.get('bids')
        else:
            glass = glass_req_result.get('asks')

        return glass if glass else None

    def get_binance_futures_history(self):  # todo стакан
        url = 'https://fapi.binance.com/fapi/v1/trades?symbol=' + self._currency_pair
        is_complete = False
        result = None
        while not is_complete:
            try:
                response = requests.get(url)
                is_complete = True
            except Exception as e:
                # self._logger.error('При получении данных из истории binance futures возникла ошибка')
                # self._logger.error(e)
                continue

            try:
                result = response.json()
            except Exception as e:
                # self._logger.error('Ошибка в попытке расшифровать json файл')
                # self._logger.error(e)
                time.sleep(2)

        return result

    def get_price(self, is_buy=True):
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

    def place_order(self, price, quantity, side):
        url = "https://testnet.binancefuture.com/fapi/v1/order"
        headers = {'X-MBX-APIKEY': self._api_key}
        data = {
            'symbol': self._currency_pair,
            'side': side,
            'type': 'LIMIT',
            "timeInForce": "GTC",
            'price': price,
            'quantity': quantity,
        }
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
            # self._logger.error('Ошибка в попытке расшифровать json файл')
            # self._logger.error(traceback.format_exc())
            # self._logger.error(e)
            # self._logger.error(response)
            return str(response)

        return result

    def place_long(self, quantity):  # todo ограничение по балансу
        price = round(self.get_price(True) * 1.2)
        result = self.place_order(price, quantity, 'BUY')
        return result

    def place_short(self, quantity):  # todo ограничение по балансу
        price = round(self.get_price(False) * 0.8)
        result = self.place_order(price, quantity, 'SELL')
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
    result = obj.get_binance_glass()
    print(result)
    # import pprint
    # pprint.pprint(result)
