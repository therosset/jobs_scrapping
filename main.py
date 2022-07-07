from dotenv import load_dotenv

from utils import get_all_offers

load_dotenv()

if __name__ == "__main__":
    raw_offers = get_all_offers("prod")
    print(raw_offers)
