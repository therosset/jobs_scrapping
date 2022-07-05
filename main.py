from pprint import pprint

from offer_class import Offer
from dotenv import load_dotenv

load_dotenv()


def get_all_offers(mode: str):
    offer = Offer(mode)
    extracted = offer.get_offer()
    return extracted


if __name__ == '__main__':
    pass
