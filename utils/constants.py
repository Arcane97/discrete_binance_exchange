import sys

ROOT_PATH = sys.path[1]  # todo потестить точно ли это кореть проекта

SETTINGS_FILE_NAME = ROOT_PATH + "\\discrete_binance_exchange_settings.json"


if __name__ == "__main__":
    print(sys.path[1])
    print(SETTINGS_FILE_NAME)
