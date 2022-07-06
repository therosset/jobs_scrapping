
class JobOffer:

    def __init__(self, offer_json: dict):
        self.job_title: str = offer_json.get("title")
        self.salary: dict = self.__set_salary_details(offer_json)
        self.company: dict = self.__set_company_details(offer_json)
        self.location: dict = self.__set_location_details(offer_json)
        self.is_remote: bool = offer_json.get("is_remote")
        self.remote_range: int = offer_json.get("remote_range")
        self.job_description: str = self.__set_description(offer_json.get("description"))

    def __set_company_details(self, offer_json: dict) -> dict:
        """Extracts company details, enriches them, puts in proper format
        returns them in dict to be set under 'company' key """
        pass

    def __set_salary_details(self, offer_json: dict) -> dict:
        """Extracts salary details, enriches them, reformats, calculates mean from max and min
        or adds max and min as mean if only mean present """
        pass

    def __set_location_details(self, offers_json: dict) -> dict:
        """Extracts location details, enriches them , reformats names to be properly encoded (polish letters etc.)
        adds some more data like Latitude and Longitude """
        pass

    def __set_description(self, description_raw: str) -> str:
        """Extracts description, parses it and makes it human readable with polish encoding, removes HTML tags etc."""
        pass

    def serialize(self):
        """Returns object as python dict just in the same form it needs to be ingested into DB"""
        return self.__dict__
