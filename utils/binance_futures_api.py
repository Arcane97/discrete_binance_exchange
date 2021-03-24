import requests

from utils.binance_base_api import BinanceBaseAPI


class BinanceFuturesAPI(BinanceBaseAPI):
    def __init__(self):
        super().__init__(dict_key_prefix='binance_futures')
        self._api_key = None
        self._api_secret = None

        self._read_api_keys_from_file()


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

    obj = BinanceFuturesAPI()

