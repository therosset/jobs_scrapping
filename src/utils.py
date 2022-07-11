import re

import requests
from dotenv import load_dotenv
from forex_python.converter import CurrencyRates

load_dotenv()

from .config import (TRANSLATE_DICT, GEO_LOCATIONS, ADDRESSES_PATTERN, \
                     CITY_PATTERN, LATITUDE_PATTERN, LONGITUDE_PATTERN, COORDINATES_TRANSLATE, EMPLOYMENTS_DICT)

from .api_connector import ApiConnector


def get_all_offers(mode: str) -> list:
    api = ApiConnector(mode)
    response = api.get_request(f"{api.url_template.format(page=1)}").json()
    max_pages = int(response['meta'].get('last_page'))
    offers = [offer for offer in response.get('data')]
    for page in range(2, max_pages + 1):
        url = f"{api.url_template.format(page=page)}"
        response = api.get_request(url)
        if response:
            offers.extend([offer for offer in response.json().get('data')])
    return offers


def enrich_data(raw_offers: list) -> list:
    from .job_model import JobOffer
    transformed = []
    for raw_offer in raw_offers:
        job_offer = JobOffer(raw_offer)
        transformed.append(job_offer.serialize())
    return transformed


def translate(text: str or None, conversion: dict or list) -> str:
    if not text:
        return text
    if isinstance(conversion, dict):
        for key, value in conversion.items():
            text = text.replace(key, value)
    elif isinstance(conversion, list):
        conversion_dict = {i: "" for i in conversion}
        for key, value in conversion_dict.items():
            text = text.replace(key, value)
    return text


def get_geo_location():
    locations = {}
    response = requests.get(url=GEO_LOCATIONS)
    addresses = re.findall(pattern=ADDRESSES_PATTERN, string=response.text, flags=re.MULTILINE)
    cities = [translate(address, TRANSLATE_DICT) for address in addresses]
    for city_raw in cities:
        city = re.search(pattern=CITY_PATTERN, string=city_raw, flags=re.MULTILINE).group().rstrip()
        geo_lat_raw = re.search(pattern=LATITUDE_PATTERN, string=city_raw, flags=re.MULTILINE).group().rstrip()
        geo_lat = translate(geo_lat_raw, COORDINATES_TRANSLATE)
        geo_long_raw = re.search(pattern=LONGITUDE_PATTERN, string=city_raw, flags=re.MULTILINE).group().rstrip()
        geo_long = translate(geo_long_raw, COORDINATES_TRANSLATE)
        locations[city] = {"lat": geo_lat, "lon": geo_long}
    return locations


def get_conversion_rates() -> dict:
    rates = CurrencyRates().get_rates('PLN')
    return rates


def set_salary(offer_json: dict, salary: int or tuple, salary_enriched: dict, employment) -> dict:
    if type(salary) == tuple:
        min_salary = get_salary_rate(offer_json, salary[0])
        max_salary = get_salary_rate(offer_json, salary[1])
        mean = (min_salary + max_salary) / 2
        salary_enriched.update({'minimal_salary_monthly': min_salary,
                                'maximal_salary_monthly': max_salary,
                                'average_salary': mean, 'employment': employment})
    else:
        salary = get_salary_rate(offer_json, salary)
        salary_enriched.update({'average_salary': salary, 'employment': employment})
    return salary_enriched


def convert_salary(rates: dict, currency: str, salary: int):
    currency: float = rates.get(currency)
    salary = salary * currency

    return salary


def convert_employment(employment: str):
    employment_converted = EMPLOYMENTS_DICT.get(employment)
    return employment_converted


def get_salary(offer_json, rates: dict):
    min_salary = offer_json.get('salary_from')
    max_salary = offer_json.get('salary_to')
    currency = offer_json.get('currency')
    salaries = (min_salary, max_salary)
    if None not in salaries:
        if currency != 'PLN':
            max_salary = convert_salary(rates=rates, currency=currency, salary=max_salary)
            min_salary = convert_salary(rates=rates, currency=currency, salary=min_salary)
        return min_salary, max_salary
    else:
        if salaries.count(None) == 2:
            return None
        else:
            salary = [i for i in salaries if i is not None][0]
            if currency != 'PLN':
                salary = convert_salary(rates=rates, currency=currency, salary=salary)
            return salary


def get_salary_rate(offer_json: dict, salary: int or tuple):
    rate = offer_json.get('rate') if salary > 999 else 'hourly'
    if rate == 'hourly':
        salary = salary * 168
    elif rate == 'yearly':
        salary = salary / 12
    else:
        return salary
    return salary
