import time
from ssl import SSLCertVerificationError

from dotenv import load_dotenv
from requests import Response
import requests
from requests.exceptions import Timeout, TooManyRedirects, ReadTimeout, ConnectTimeout, SSLError
from .config import response_dict

load_dotenv()


class ApiConnector:

    def __init__(self, mode: str):
        self.sleep_sec: int = 0
        self.back_of_factor: int = 0
        self.max_retries: int = 0
        self.url_template: str = "https://api.4programmers.net/v1/jobs?page={page}"
        self.set_mode(mode)

    def set_mode(self, mode: str):
        if mode == "test":
            self.sleep_sec = 120
            self.back_of_factor = 5
            self.max_retries = 20
        else:
            self.max_retries = 5
            self.back_of_factor = 3

    def get_request(self, url: str) -> Response:
        status_code = 0
        tries = 1
        while status_code != 200 and tries <= self.max_retries:
            try:
                response = requests.get(url, headers={'accept': 'application/json'})
                status_code = response.status_code
                print(f" Retry number {tries}/{self.max_retries} Sending request to: {url}, response: {status_code}")
                if not self._handle_errors(status_code, tries):
                    return response
            except Exception as e:
                print(url)
                self._handle_exceptions(e, tries)
            finally:
                tries += 1

    def _handle_errors(self, status_code, retries) -> bool:
        if status_code == 429:
            sleep = self.sleep_sec + retries * self.back_of_factor
            print(response_dict.get(status_code).format(time=sleep))
            time.sleep(self.sleep_sec + retries * self.back_of_factor)
            return True
        if status_code >= 500:
            print(response_dict.get(status_code))
            return True
        if status_code == 403:
            print(response_dict.get(status_code))
            return True
        else:
            return False

    def _handle_exceptions(self, e: Exception, retries) -> bool:
        if e in (Timeout, TooManyRedirects, ReadTimeout, ConnectTimeout, SSLError, SSLCertVerificationError):
            print(f"Exception : {e}")
            print(f"Sleep :{self.sleep_sec + retries * self.back_of_factor}s")
            time.sleep(self.sleep_sec + retries * self.back_of_factor)
            return True
        else:
            raise e
