from dotenv import load_dotenv
load_dotenv()

from src.elasticsearch_connector import ElasticsearchConnector
from src.utils import (get_all_offers, enrich_data)

es_client = ElasticsearchConnector(local=True)

if __name__ == "__main__":
    offers = get_all_offers(mode="prod")
    enriched_messages = enrich_data(offers)
    es_client.send_separately(message_list=enriched_messages)

