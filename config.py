import os

ELK_LOCAL_URL = os.environ["ELK_LOCAL_URL"]
ELK_PASSWORD = os.environ["ELK_PASSWORD"]
ELK_USERNAME = os.environ["ELK_USERNAME"]
ELK_REMOTE_IP = os.environ["ELK_REMOTE_IP"]

ELASTICSEARCH_MAX_TIMEOUT_IN_SECONDS = 500
INDEX_DATE_FMT = "%Y-%m-%d"
MAX_CHUNK_SIZE_IN_BYTES = 100000000000  # 100MB
INGEST_DATA_MAXIMUM_RETRIES = 5
INGEST_DATA_INIT_BACKOFF = 2
INGEST_DATA_MAX_BACKOFF = 30
CHUNK_SIZE = 500

response_dict = {400: 'Bad request',
                 401: 'Unauthorized',
                 403: 'Forbidden',
                 404: 'Data not found',
                 405: 'Method not allowed',
                 415: 'Unsupported media type',
                 429: 'Rate limit exceeded, another try in {time}s',
                 500: 'Internal server error',
                 502: 'Bad gateway',
                 503: 'Service unavailable',
                 504: 'Gateway timeout'
                 }
