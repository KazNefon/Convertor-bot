import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты: {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        url = f'https://v6.exchangerate-api.com/v6/ae5a279d6ebf1651308c6a04/pair/{quote_ticker}/{base_ticker}'
        response = requests.get(url)
        data = json.loads(response.content)

        if 'conversion_rate' not in data:
            raise ConvertionException('Ошибка при получении курса валют')

        conversion_rate = data['conversion_rate']
        total_base = amount * conversion_rate
        return total_base
