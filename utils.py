from dotenv import load_dotenv

from job_model import JobOffer

load_dotenv()
from api_connector import ApiConnector


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
