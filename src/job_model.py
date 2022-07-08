from .config import (TRANSLATE_DICT_SPECIAL_SIGNS, TAGS_REMOVE, CITIES_TRANSLATE)


class JobOffer:
    from .utils import get_geo_location
    locations = get_geo_location()

    def __init__(self, offer_json: dict):
        self.job_title: str = offer_json.get("title")
        self.seniority: str = offer_json.get("seniority")
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
        """Extracts salary details, enriches them, reformat, calculates mean from max and min
        or adds max and min as mean if only mean present """
        pass

    def __set_location_details(self, offers_json: dict) -> dict:
        """Extracts location details, enriches them , reformat names to be properly encoded (polish letters etc.)
        adds some more data like Latitude and Longitude """
        from .utils import translate
        try:
            city_raw = offers_json["locations"][0].get("city")
            city = translate(city_raw, CITIES_TRANSLATE)
            loc_details = offers_json["locations"][0]
            coordinates = self.locations.get(city)
            return {"city": city, "loc_details": loc_details, "coordinates": coordinates}
        except IndexError as e:
            print(f"No location given for:{offers_json['locations']}: {e}")

    def __set_description(self, description_raw: str) -> str:
        """Extracts description, parses it and makes it human-readable with polish encoding, removes HTML tags etc."""
        from .utils import translate
        tags_removed = translate(description_raw, TAGS_REMOVE)
        translated = translate(tags_removed.encode('utf-8', 'replace').decode(), TRANSLATE_DICT_SPECIAL_SIGNS)
        return translated

    def serialize(self):
        """Returns object as python dict just in the same form it needs to be ingested into DB"""
        return self.__dict__
