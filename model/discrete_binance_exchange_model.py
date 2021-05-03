from math import isclose
from PyQt5.QtCore import QObject, pyqtSignal

from utils.constants import BINANCE_SPOT_FILTERS, BINANCE_FUTURES_FILTERS


class DiscreteBinanceExchangeModel(QObject):
    """ Класс реализующий покупку или продажу валюты на бирже Binance.
    Сделки совершаются маленькими порциями.
    Порцией является заданое количество валюты деленное на число разбиений.
    При продаже валюты на спотовом рынке, берется лонг (закрывается шорт).
    При покупке на спотовом рынке, берется шорт (закрывается лонг).
    """
    def __init__(self):
        super().__init__()

        # тип сделки (покупка или продажа)
        self._deal_type = "SELL"
        # валютная пара
        self._currency_pair = "BTCUSDT"
        # количество валюты на спотовом рынке
        self._currency_amount_spot = 2
        # количество валюты во фьючерсах
        self._currency_amount_futures = 2
        # число разбиений
        self._number_of_splits = 10

        # считываем параметры из файла
        self._read_param_file()

        # флаг. запущены торги
        self._is_running_trades = True

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
        print(amount)

    def start_trades(self):
        """ Старт торгов с разбиением
        """
        self._is_running_trades = True
        # количество цифр после запятой у минимального количества валюты
        exponent = -max(BINANCE_SPOT_FILTERS[self._currency_pair]['minQtyExponent'],
                        BINANCE_FUTURES_FILTERS[self._currency_pair]['minQtyExponent'])
        # минимальное количество валюты
        min_qty = max(BINANCE_SPOT_FILTERS[self._currency_pair]['minQty'],
                      BINANCE_FUTURES_FILTERS[self._currency_pair]['minQty'])
        # количество валюты в порции
        delta_amount = round(self._currency_amount_spot / self._number_of_splits, exponent)
        if delta_amount < min_qty:
            print('Сделайте меньше разбиений')  # todo Лог
            return

        while self._is_running_trades and \
                self._currency_amount_spot > min_qty and self._currency_amount_futures > min_qty:
            # если после следующей сделки количество валюты будет меньше минимума,
            # используем всю оставшуюся валюту
            if min(self._currency_amount_spot, self._currency_amount_futures) - delta_amount < min_qty:
                delta_amount = round(min(self._currency_amount_spot, self._currency_amount_futures), exponent)

            self._trade(delta_amount)

            self.currency_amount_spot -= delta_amount
            self.currency_amount_futures -= delta_amount

    def stop_trades(self):
        """ Принудительная остановка торгов
        """
        self._is_running_trades = False

    def save_param_to_file(self):
        """ Сохранение параметров в файл
        """
        pass


if __name__ == "__main__":
    obj = DiscreteBinanceExchangeModel()
    obj.start_trades()
