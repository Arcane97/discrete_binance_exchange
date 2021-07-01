import logging
from math import isclose
from PyQt5.QtCore import QObject, pyqtSignal

from utils.binance_futures_api import BinanceFuturesAPI
from utils.binance_spot_api import BinanceSpotAPI
from utils.constants import BINANCE_SPOT_FILTERS, BINANCE_FUTURES_FILTERS


class DiscreteBinanceExchangeModel(QObject):
    """ Класс реализующий покупку или продажу валюты на бирже Binance.
    Сделки совершаются маленькими порциями.
    Порцией является заданое количество валюты деленное на число разбиений.
    При продаже валюты на спотовом рынке, берется лонг (закрывается шорт).
    При покупке на спотовом рынке, берется шорт (закрывается лонг).
    """
    def __init__(self, deal_type, currency_pair, currency_amount_spot, currency_amount_futures, number_of_splits,
                 logger_name="discrete_binance_exchange"):
        super().__init__()

        # тип сделки (покупка или продажа)
        self._deal_type = deal_type
        # валютная пара
        self._currency_pair = currency_pair
        # количество валюты на спотовом рынке
        self._currency_amount_spot = currency_amount_spot
        # количество валюты во фьючерсах
        self._currency_amount_futures = currency_amount_futures
        # число разбиений
        self._number_of_splits = number_of_splits

        # считываем параметры из файла
        self._read_param_file()

        # логгер
        self._logger = logging.getLogger(logger_name)

        # флаг. запущены торги
        self._is_running_trades = True

        # апи спотового рынка
        self._binance_spot_api = BinanceSpotAPI(deal_type, currency_pair, logger_name)
        # апи фьючерсов
        self._binance_futures_api = BinanceFuturesAPI(deal_type, currency_pair)

        # количество валюты на спотовом рынке изменилось
        self._currency_amount_spot_changed = pyqtSignal()
        # количество валюты на фьючерсах изменилось
        self._currency_amount_futures_changed = pyqtSignal()

    @property
    def deal_type(self):
        return self._deal_type

    @deal_type.setter
    def deal_type(self, val):
        self._deal_type = val

    @property
    def currency_pair(self):
        return self._currency_pair

    @currency_pair.setter
    def currency_pair(self, val):
        self._currency_pair = val

    @property
    def currency_amount_spot(self):
        return self._currency_amount_spot

    @currency_amount_spot.setter
    def currency_amount_spot(self, val):
        if not isclose(self._currency_amount_spot, val, rel_tol=0, abs_tol=0.001):
            self._currency_amount_spot = val
            self._currency_amount_spot_changed.emit()
        else:
            self._currency_amount_spot = val

    @property
    def currency_amount_futures(self):
        return self._currency_amount_futures

    @currency_amount_futures.setter
    def currency_amount_futures(self, val):
        if not isclose(self._currency_amount_futures, val, rel_tol=0, abs_tol=0.001):
            self._currency_amount_futures = val
            self._currency_amount_futures_changed.emit()
        else:
            self._currency_amount_futures = val

    @property
    def number_of_splits(self):
        return self._number_of_splits

    @number_of_splits.setter
    def number_of_splits(self, val):
        self._number_of_splits = val

    def _read_param_file(self):
        """ Считываение параметров из файла
        """
        pass

    def _trade(self, amount: float):
        """ Выполнение торга
        :param amount: количество
        """
        self._logger.info(f'Выполнение торгов. Количество {amount}')

        spot_result = self._binance_spot_api.place_order(amount)
        self._logger.info(f'Результат выполнения торга на спотовом рынке: {spot_result}')

        futures_result = self._binance_futures_api.place_order(amount)
        self._logger.info(f'Результат выполнения торга на фьючерсном рынке: {futures_result}')

    def start_trades(self):
        """ Старт торгов с разбиением
        """
        self._logger.info(f'Старт торгов с разбиением. Тип: {self.deal_type}. Пара: {self._currency_pair}. '
                          f'Количество валюты на спотовом рынке: {self._currency_amount_spot} '
                          f'Количество валюты на фьючерсном рынке: {self._currency_amount_futures} '
                          f'Количество разбиений: {self._number_of_splits}')
        self._is_running_trades = True
        # количество цифр после запятой у минимального количества валюты
        exponent = -max(BINANCE_SPOT_FILTERS[self._currency_pair]['minQtyExponent'],
                        BINANCE_FUTURES_FILTERS[self._currency_pair]['minQtyExponent'])
        self._logger.debug(f'Экспонента: {exponent}')
        # минимальное количество валюты
        min_qty = max(BINANCE_SPOT_FILTERS[self._currency_pair]['minQty'],
                      BINANCE_FUTURES_FILTERS[self._currency_pair]['minQty'])
        self._logger.debug(f'Минимальное количество валюты: {min_qty}')
        # количество валюты в порции
        delta_amount = round(self._currency_amount_spot / self._number_of_splits, exponent)
        self._logger.debug(f'Количество валюты в порции: {delta_amount}')
        if delta_amount < min_qty:
            self._logger.info(f'Сделайте меньше разбиений! '
                              f'Максимальное количество разбиений на данное количество валюты: '
                              f'{round(self._currency_amount_spot / min_qty)}')
            return

        while self._is_running_trades and \
                self._currency_amount_spot > min_qty and self._currency_amount_futures > min_qty:
            # если после следующей сделки количество валюты будет меньше минимума,
            # используем всю оставшуюся валюту
            if min(self._currency_amount_spot, self._currency_amount_futures) - delta_amount < min_qty:
                delta_amount = round(min(self._currency_amount_spot, self._currency_amount_futures), exponent)
                self._logger.info(f'Валюты останось мало, поэтому используем всю оставшуюся валюту: {delta_amount}')

            self._trade(delta_amount)

            self.currency_amount_spot -= delta_amount
            self.currency_amount_futures -= delta_amount
            self._logger.info(f'После торгов останось: Спот: {self._currency_amount_spot} Фьючерс: {self._currency_amount_futures}')
            # todo задержка между торгами?

        self._logger.info('Конец торгов с разбиением')

    def stop_trades(self):
        """ Принудительная остановка торгов
        """
        self._is_running_trades = False
        self._logger.info('Принудительная остановка торгов')

    def save_param_to_file(self):
        """ Сохранение параметров в файл
        """
        pass


if __name__ == "__main__":
    obj = DiscreteBinanceExchangeModel("SELL", "BTCUSDT", 2, 2, 10)
    obj.start_trades()
