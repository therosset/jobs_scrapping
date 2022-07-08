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
        self.tech_tags: list = self.__find_tech_tags()
        self.job_simplified: str = self.__set_simplified_job_field()
        self.created_at: str = offer_json.get("created_at")
        self.deadline_at: str = offer_json.get("deadline_at")

    def __set_company_details(self, offer_json: dict) -> dict:
        from .utils import translate
        """Extracts company details, enriches them, puts in proper format
        returns them in dict to be set under 'company' key """
        company = offer_json.get("firm")
        if company:
            description_no_tags = translate(offer_json.get("description"), TAGS_REMOVE)
            description_translated = translate(description_no_tags, TRANSLATE_DICT_SPECIAL_SIGNS)
            company_yt_link = translate(company.get("youtube_url"), TRANSLATE_DICT_SPECIAL_SIGNS)
            company_url = translate(company.get("url"), TRANSLATE_DICT_SPECIAL_SIGNS)
            city = company.get("city")
            if city:
                city_translated = translate(city, CITIES_TRANSLATE)
                city_coordinates = self.locations.get(city_translated)
            else:
                city_translated = ""
                city_coordinates = {}
            return {"name": company.get("name"), "description": description_translated, "Youtube": company_yt_link,
                    "url": company_url, "city": city_translated, "company_coordinates": city_coordinates}

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

    def __find_tech_tags(self) -> list:
        from .config import TECHNOLOGY_LIST
        tags = []
        job_description = self.job_description.lower()
        for tech in TECHNOLOGY_LIST:
            if tech.lower() in job_description:
                tags.append(tech.lower())
        return tags

    def __set_simplified_job_field(self) -> str:
        from .config import SIMPLIFIED_JOBS_DESC
        job_title = self.job_title.lower()
        for job_tag in SIMPLIFIED_JOBS_DESC:
            if job_tag in job_title:
                return job_tag.strip("-")

    def serialize(self):
        """Returns object as python dict just in the same form it needs to be ingested into DB"""
        return self.__dict__
