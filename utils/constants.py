from definitions import ROOT_DIR

SETTINGS_FILE_NAME = ROOT_DIR + "\\discrete_binance_exchange_settings.json"

BINANCE_SPOT_FILTERS = {'BNBBTC': {'minPrice': 1e-07, 'minQty': 0.01, 'minQtyExponent': -2},
                        'BNBBUSD': {'minPrice': 0.0001, 'minQty': 0.01, 'minQtyExponent': -2},
                        'BNBUSDT': {'minPrice': 0.0001, 'minQty': 0.01, 'minQtyExponent': -2},
                        'BTCBUSD': {'minPrice': 0.01, 'minQty': 1e-06, 'minQtyExponent': -6},
                        'BTCUSDT': {'minPrice': 0.01, 'minQty': 1e-06, 'minQtyExponent': -6},
                        'ETHBTC': {'minPrice': 1e-06, 'minQty': 1e-05, 'minQtyExponent': -5},
                        'ETHBUSD': {'minPrice': 0.01, 'minQty': 1e-05, 'minQtyExponent': -5},
                        'ETHUSDT': {'minPrice': 0.01, 'minQty': 1e-05, 'minQtyExponent': -5},
                        'LTCBNB': {'minPrice': 0.001, 'minQty': 1e-05, 'minQtyExponent': -5},
                        'LTCBTC': {'minPrice': 1e-06, 'minQty': 1e-05, 'minQtyExponent': -5},
                        'LTCBUSD': {'minPrice': 0.01, 'minQty': 1e-05, 'minQtyExponent': -5},
                        'LTCUSDT': {'minPrice': 0.01, 'minQty': 1e-05, 'minQtyExponent': -5},
                        'TRXBNB': {'minPrice': 1e-06, 'minQty': 0.1, 'minQtyExponent': -1},
                        'TRXBTC': {'minPrice': 1e-08, 'minQty': 0.1, 'minQtyExponent': -1},
                        'TRXBUSD': {'minPrice': 1e-05, 'minQty': 0.1, 'minQtyExponent': -1},
                        'TRXUSDT': {'minPrice': 1e-05, 'minQty': 0.1, 'minQtyExponent': -1},
                        'XRPBNB': {'minPrice': 1e-05, 'minQty': 0.1, 'minQtyExponent': -1},
                        'XRPBTC': {'minPrice': 1e-08, 'minQty': 0.1, 'minQtyExponent': -1},
                        'XRPBUSD': {'minPrice': 1e-05, 'minQty': 0.1, 'minQtyExponent': -1},
                        'XRPUSDT': {'minPrice': 1e-05, 'minQty': 0.1, 'minQtyExponent': -1}}

BINANCE_FUTURES_FILTERS = {
    '1INCHUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'AAVEUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'ADAUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'AKROUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'ALGOUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'ALICEUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'ALPHAUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'ANKRUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'ATOMUSDT': {'minPrice': 0.001, 'minQty': 0.01, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -2},
    'AVAXUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'AXSUSDT': {'minPrice': 0.001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'BALUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'BANDUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'BATUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'BCHUSDT': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'BELUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'BLZUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'BNBUSDT': {'minPrice': 0.001, 'minQty': 0.01, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -2},
    'BTCBUSD': {'minPrice': 0.1, 'minQty': 0.001, 'multiplierDown': 0.95, 'multiplierUp': 1.05, 'minQtyExponent': -3},
    'BTCSTUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'BTCUSDT': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'BTCUSDT_210625': {'minPrice': 0.1, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15,
                       'minQtyExponent': -3},
    'BTSUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'BTTUSDT': {'minPrice': 1e-06, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'BZRXUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'CELRUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'CHRUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'CHZUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'COMPUSDT': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'COTIUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'CRVUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'CTKUSDT': {'minPrice': 0.001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'CVCUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'DASHUSDT': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'DEFIUSDT': {'minPrice': 0.1, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'DENTUSDT': {'minPrice': 1e-06, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'DGBUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'DODOUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'DOGEUSDT': {'minPrice': 1e-06, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'DOTUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'EGLDUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'ENJUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'EOSUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'ETCUSDT': {'minPrice': 0.001, 'minQty': 0.01, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -2},
    'ETHUSDT': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'ETHUSDT_210625': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15,
                       'minQtyExponent': -3},
    'FILUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'FLMUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'FTMUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'GRTUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'HBARUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'HNTUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'HOTUSDT': {'minPrice': 1e-06, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'ICXUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'IOSTUSDT': {'minPrice': 1e-06, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'IOTAUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'KAVAUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'KNCUSDT': {'minPrice': 0.001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'KSMUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'LINAUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'LINKUSDT': {'minPrice': 0.001, 'minQty': 0.01, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -2},
    'LITUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'LRCUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'LTCUSDT': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'LUNAUSDT': {'minPrice': 0.001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'MANAUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'MATICUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'MKRUSDT': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'MTLUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'NEARUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'NEOUSDT': {'minPrice': 0.001, 'minQty': 0.01, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -2},
    'NKNUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'OCEANUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'OGNUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'OMGUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'ONEUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'ONTUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'QTUMUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'REEFUSDT': {'minPrice': 1e-06, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'RENUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'RLCUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'RSRUSDT': {'minPrice': 1e-06, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'RUNEUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'RVNUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'SANDUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'SCUSDT': {'minPrice': 1e-06, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'SFPUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'SKLUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'SNXUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'SOLUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'SRMUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'STMXUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'STORJUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'SUSHIUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'SXPUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'THETAUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15,
                  'minQtyExponent': -1},
    'TOMOUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'TRBUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'TRXUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'UNFIUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'UNIUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'VETUSDT': {'minPrice': 1e-06, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'WAVESUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15,
                  'minQtyExponent': -1},
    'XEMUSDT': {'minPrice': 0.0001, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'XLMUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'XMRUSDT': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'XRPUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'XTZUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'YFIIUSDT': {'minPrice': 0.1, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'YFIUSDT': {'minPrice': 0.1, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'ZECUSDT': {'minPrice': 0.01, 'minQty': 0.001, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -3},
    'ZENUSDT': {'minPrice': 0.001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1},
    'ZILUSDT': {'minPrice': 1e-05, 'minQty': 1.0, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': 0},
    'ZRXUSDT': {'minPrice': 0.0001, 'minQty': 0.1, 'multiplierDown': 0.85, 'multiplierUp': 1.15, 'minQtyExponent': -1}}


if __name__ == "__main__":
    print(SETTINGS_FILE_NAME)
    # import decimal
    #
    # new_d = {}
    # for key, value in BINANCE_FUTURES_FILTERS.items():
    #     value['minQtyExponent'] = decimal.Decimal(str(value['minQty']).rstrip('0')).as_tuple().exponent
    #     new_d[key] = value
    # print(new_d)

    # for key, value in BINANCE_SPOT_FILTERS.items():
    #     if key in BINANCE_FUTURES_FILTERS.keys():
    #         print(key, 'spot: ', value['minQty'], decimal.Decimal(str(value['minQty']).rstrip('0')).as_tuple().exponent, ' futures: ', BINANCE_FUTURES_FILTERS[key]['minQty'], decimal.Decimal(str(BINANCE_FUTURES_FILTERS[key]['minQty']).rstrip('0')).as_tuple().exponent)
