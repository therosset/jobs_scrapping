from dotenv import load_dotenv
load_dotenv()

from src.elasticsearch_connector import ElasticsearchConnector
from src.utils import (get_all_offers, enrich_data)


#es_cient = ElasticsearchConnector(local=True)

if __name__ == "__main__":
    offers = get_all_offers(mode="prodd")
    enriched = enrich_data(offers)
    print(enriched)
