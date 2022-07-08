from dotenv import load_dotenv

from src.utils import (get_all_offers, enrich_data)

load_dotenv()

if __name__ == "__main__":

    offers = get_all_offers(mode="prodd")
    enriched = enrich_data(offers)
    print(enriched)
