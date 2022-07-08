import datetime

from elasticsearch import RequestsHttpConnection
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

from migration_script.config import ELK_URL
from .config import ELASTICSEARCH_MAX_TIMEOUT_IN_SECONDS, INGEST_DATA_MAX_BACKOFF, \
    INGEST_DATA_INIT_BACKOFF, CHUNK_SIZE, INGEST_DATA_MAXIMUM_RETRIES, ELK_PASSWORD, ELK_USERNAME, INDEX_DATE_FMT, \
    ELK_REMOTE_IP


class ElasticsearchConnector:
    def __init__(self, local: bool):
        self.es_client = self.__setup_client(local)

    def __setup_client(self, local: bool):
        es_client = Elasticsearch(
            hosts=[{'host': ELK_URL if not local else ELK_REMOTE_IP, 'port': 9200}],
            http_auth=(ELK_USERNAME, ELK_PASSWORD),
            scheme='https',
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            retry_on_timeout=True,
            timeout=ELASTICSEARCH_MAX_TIMEOUT_IN_SECONDS
        )
        return es_client

    @staticmethod
    def __create_msg_batches(messages: list, batch_size: int) -> list:
        return [messages[i * batch_size:(i + 1) * batch_size] for i in
                range((len(messages) + batch_size - 1) // batch_size)]

    def send_messages(self, message_list: list, batch_size: int):
        msg_batches = self.__create_msg_batches(message_list, batch_size)
        for batch in msg_batches:
            date = datetime.datetime.strftime(datetime.datetime.now(), INDEX_DATE_FMT)
            resp = bulk(
                client=self.es_client,
                doc_type="_doc",
                index=f"jobs-scrapped-{date}",
                actions=batch,
                max_retries=INGEST_DATA_MAXIMUM_RETRIES,
                raise_on_error=False,
                chunk_size=CHUNK_SIZE,
                initial_backoff=INGEST_DATA_INIT_BACKOFF,
                max_backoff=INGEST_DATA_MAX_BACKOFF
            )
            print(f"Sending: {len(message_list)}, response: {resp}")
