from api_connector import ApiConnector
from collections import namedtuple


class Offer(ApiConnector):

    def get_offer(self, page=1) -> list:
        entries = []
        offers = []
        data = [1]
        while len(data) != 0:
            url = f"{self.url_template.format(page=page)}"
            response = self._get_request(url)
            data = response.json().get('data')
            try:
                entries.extend(data)
                page += 1
                for i in entries:
                    # converting json to object
                    offer = namedtuple("Offer", i.keys())(*i.values())
                    offers.append(offer)
            except TypeError as e:
                print(f'missing parameters: {e}')
        return offers
