from math import isclose
from PyQt5.QtCore import QObject, pyqtSignal


class DiscreteBinanceExchangeModel(QObject):
    """ Класс реализующий покупку или продажу валюты на бирже Binance.
    Сделки совершаются маленькими порциями.
    Порцией является заданое количество валюты деленное на число разбиений.
    При продаже валюты на спотовом рынке, берется лонг (закрывается шорт).
    При покупке на спотовом рынке, берется шорт (закрывается лонг).
    """
    # количество валюты изменилось
    currency_amount_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        # тип сделки (покупка или продажа)
        self._deal_type = "SELL"
        # валютная пара
        self._currency_pair = "BTCUSDT"
        # количество валюты
        self._currency_amount = 2
        # число разбиений
        self._number_of_splits = 10

        # считываем параметры из файла
        self._read_param_file()

        # флаг. запущены торги
        self._is_running_trades = True

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
    def currency_amount(self):
        return self._currency_amount

    @currency_amount.setter
    def currency_amount(self, val):
        if not isclose(self._currency_amount, val, rel_tol=0, abs_tol=0.001):
            self._currency_amount = val
            self.currency_amount_changed.emit()
        else:
            self._currency_amount = val

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
        delta_amount = round(self._currency_amount / self._number_of_splits, 3)
        if delta_amount < 0.001:
            print('Сделайте меньше разбиений')  # todo Лог
            return

        while self._is_running_trades and self._currency_amount > 0.001:
            if self._currency_amount - delta_amount < 0.002:
                delta_amount = round(self._currency_amount, 3)

            self._trade(delta_amount)

            self.currency_amount -= delta_amount

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
