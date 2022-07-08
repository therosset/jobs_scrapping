import re

import requests
from dotenv import load_dotenv

load_dotenv()

from .config import (TRANSLATE_DICT, GEO_LOCATIONS, ADDRESSES_PATTERN, \
                                               CITY_PATTERN, LATITUDE_PATTERN, LONGITUDE_PATTERN, COORDINATES_TRANSLATE)

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


def translate(text: str, conversion: dict or list) -> str:
    if isinstance(conversion, dict):
        for key, value in conversion.items():
            text = text.replace(key, value)
    elif isinstance(conversion, list):
        conversion_dict = {i: "" for i in conversion}
        for key, value in conversion_dict.items():
            text = text.replace(key, value)
    return text


def get_geo_location():
    print("Starting locations")
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
        locations[city] = {"coordinates": {"geo_lat": geo_lat, "geo_long": geo_long}}
    return locations

