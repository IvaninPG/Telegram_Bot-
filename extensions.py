import json
import requests
from config import keys

class ConvertionException(Exception):
    pass

class СurrencyConverter:
    @staticmethod
    def convert(from_: str, to_: str, amount: str):

        try:
            from_abbrev = keys[from_]
        except KeyError:
            raise ConvertionException(f'Не удалось выбрать валюту "{from_}"')

        try:
            to_abbrev = keys[to_]
        except KeyError:
            raise ConvertionException(f'Не удалось выбрать валюту "{to_}"')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать колличество "{amount}"')

        r = requests.get('http://api.exchangeratesapi.io/v1/latest?access_key=2194d2cb94b66ee29f2947c75cdcd05d')
        rates = json.loads(r.content)['rates']
        total_base = round(float(rates[to_abbrev]) / float(rates[from_abbrev]) * float(amount), 2)

        return total_base