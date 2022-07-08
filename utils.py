from dotenv import load_dotenv

from job_model import JobOffer

load_dotenv()
from api_connector import ApiConnector
from forex_python.converter import CurrencyRates


def get_all_offers(mode: str) -> list:
    api = ApiConnector(mode)
    response = api.get_request(f"{api.url_template.format(page=1)}").json()
    max_pages = int(response['meta'].get('last_page'))
    offers = [offer for offer in response.get('data')]
    for page in range(2, max_pages + 1):
        url = f"{api.url_template.format(page=page)}"
        response = api.get_request(url).json()
        offers.extend([offer for offer in response.get('data')])
    return offers


def enrich_data(raw_offers: list) -> list:
    transformed = []
    for raw_offer in raw_offers:
        job_offer = JobOffer(raw_offer)
        transformed.append(job_offer)
    return transformed


def currency_converter():
    return CurrencyRates()


def salary_details(offer_json: dict):
    converter = currency_converter()
    salary_enriched = {}
    min_salary: int = offer_json.get('salary_from')
    max_salary: int = offer_json.get('salary_to')
    employment: str = offer_json.get('employment')

    if not [x for x in (min_salary, max_salary) if x is None]:
        is_gross = offer_json.get('is_gross')
        rate = offer_json.get('rate') if max_salary > 3 else 'hourly'
        currency: str = offer_json.get('currency')
        if rate == 'yearly':
            min_salary = int(min_salary / 12)
            max_salary = int(max_salary / 12)
        elif rate == 'hourly':
            min_salary = min_salary * 168
            max_salary = max_salary * 168

        # potential conversion to PLN
        if currency.upper() != 'PLN':
            max_salary = int(converter.convert(base_cur=currency, dest_cur='PLN', amount=max_salary))
            min_salary = int(converter.convert(base_cur=currency, dest_cur='PLN', amount=min_salary))

        mean = max_salary + min_salary / 2 if min_salary != max_salary else min_salary + max_salary

        salary_enriched.update({'minimal_salary_monthly': min_salary, 'maximum_salary_monthly': max_salary,
                                'average_salary': mean, 'employment': employment, 'is_gross': is_gross})
    elif max_salary is not None and min_salary is None:
        is_gross = offer_json.get('is_gross')
        rate = offer_json.get('rate') if max_salary > 3 else 'hourly'
        currency: str = offer_json.get('currency')
        if rate == 'yearly':
            max_salary = int(max_salary / 12)
        else:
            max_salary = max_salary * 168

        if currency.upper() != 'PLN':
            max_salary = int(converter.convert(base_cur=currency, dest_cur='PLN', amount=max_salary))

        mean = max_salary
        salary_enriched.update({'average_salary': mean, 'employment': employment, 'is_gross': is_gross})

    elif min_salary is not None and max_salary is None:
        is_gross = offer_json.get('is_gross')
        rate = offer_json.get('rate') if min_salary > 3 else 'hourly'
        currency: str = offer_json.get('currency')
        if rate == 'yearly':
            min_salary = int(min_salary / 12)
        else:
            min_salary = min_salary * 168

        if currency.upper() != 'PLN':
            min_salary = int(converter.convert(base_cur=currency, dest_cur='PLN', amount=min_salary))

        mean = min_salary
        salary_enriched.update({'average_salary': mean, 'employment': employment, 'is_gross': is_gross})

    else:
        salary_enriched.update({'employment': employment})

    return salary_enriched
