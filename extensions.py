import requests
import json
from config import unit, api_key


class APIException(Exception):
    """Класс исключения для вызова ошибки пользователя"""
    pass


class ExchangeRate():
    """Класс конвертации валют.
    Метод get_prise отлавливает исключения, возвращает пользователю результат конвертации"""

    @staticmethod
    def get_prise(base: str, target: str, amount: str):

        if base == target:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}')

        try:
            base_ticker = unit[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}".')

        try:
            target_ticker = unit[target]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{target}".')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}".')

        url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_ticker}/{target_ticker}/{amount}'
        r = requests.get(url)
        total_target = json.loads(r.content)['conversion_result']

        return total_target
