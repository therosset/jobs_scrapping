from dotenv import load_dotenv
from job_model import JobOffer
from utils import get_all_offers, enrich_data


load_dotenv()

if __name__ == "__main__":
    data = enrich_data(get_all_offers('prod'))
    # raw_offers = get_all_offers("prod")
    for i in data:
        print(i.__dict__)

