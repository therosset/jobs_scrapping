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

GEO_LOCATIONS = "https://astronomia.zagan.pl/art/wspolrzedne.html"

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
TRANSLATE_DICT = {"¯": "Ż", "³": "ł", "æ": "ć", "¶": "ś", "±": "ą", "¦": "Ś", "ñ": "ń", "ê": "ę", "£": "Ł", "¿": "ż",
                  "¼": "ź"}
COORDINATES_TRANSLATE = {"°": ".", "E": "", "N": "", "'": ""}
CITIES_TRANSLATE = {"Варшава": "Warszawa", "Warsaw": "Warszawa", "Krakow": "Kraków", "Wroclaw": "Wrocław",
                    "Gdansk": "Gdańsk"}
TRANSLATE_DICT_SPECIAL_SIGNS = {"&amp;": "&", "\u0119": "ę", "\\u014": "ł", "\u0105": "ą", "\u0107": "ć", "\u00f3": "ó",
                                "\/": "/"}
TAGS_REMOVE = ["<pre>", "</pre>", "<PRE>", "</PRE>", "<br />", "<br >", "\r", "\n", "<li>", "</li>", "<b>", "</b>",
               "<strong>", "</strong>", "<div>", "</div>", "<ul>", "</ul>", "<\/strong>", "<br \/>", "<\/li>", "<\/ul>",
               "\xa0"]

CITY_PATTERN = "(?<=)(.*?)(?=\d\d°\d\d'E)"
ADDRESSES_PATTERN = "(?<='N\n)(.*?N)(?=\n)"
LATITUDE_PATTERN = "(\d\d°\d\d'E)"
LONGITUDE_PATTERN = "(\d\d°\d\d'N)"

TECHNOLOGY_LIST = ["C ", "java", "python", "C++", "C#", ".Net", "Kotlin", "Scala", "Objective-c", "Swift", "React",
                   "Flutter", "Ionic", "Cordova", "Javascript", "Ruby", "PHP", "Spring", "Elixir", "Perl", "MySQL",
                   "MSSQL", "SQL", "SqlLite", "Mongo", "Cassandra", "Elasticsearch", "T-Sql", "ASP.NET", "Redis",
                   "Neo4j", "React4j", "VueJs", "Angular", "Web Components", "AWS", "AZURE", "GCP", "Docker",
                   "Kubernetes", "HTML", "CSS", "django", "flask", "fastapi", "Heroku", "jquery", "bootstrap", "MVC",
                   "WebApi", "hadoop", "spark", "kafka", "queue", "j2ee", "oracle", "powerbi", "tableu", "rmq",
                   "Rabbitmq", "hibernate", "PostgreSQL", "Derby", "LDAP", "Tomcat", "JBoss", "selenium", "blockchain",
                   "machine learning", "Jenkins", "Git", "sre","Helm","Ansible","Terraform"]

SIMPLIFIED_JOBS_DESC = ["frontend", "fron-end" "backend", "back-end", "admin", "devops", "dev-ops", "project", "team",
                        "scrum", "data", "cloud", "ops", "developer", "engineer", "iot", "product owner", "manager",
                        "director"]
