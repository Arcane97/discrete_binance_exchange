import json, requests

from utils.constants import SETTINGS_FILE_NAME


class BinanceSpotAPI:
    def __init__(self):
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

    obj = BinanceSpotAPI()

