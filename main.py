from api_connector import ApiConnector
from dotenv import load_dotenv

load_dotenv()


def get_all_offers(mode: str) -> list:
    api = ApiConnector(mode)
    page_num = 1
    responses = []
    entries = []
    url = f"{api.url_template.format(page=page_num)}"
    response = api._get_request(url)
    data = response.json()
    page_amount = data.get('meta')['last_page']
    if page_num <= page_amount:
        for page in range(page_amount):
            url = f"{api.url_template.format(page=page)}"
            response = api._get_request(url)
            responses.append(response.json())
            page_num += 1
    for response in responses:
        offer = response.get('data')
        entries.extend(offer)

    return entries


if __name__ == '__main__':
    pass
