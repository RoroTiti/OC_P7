import random
from abc import abstractmethod, ABCMeta

import requests
from regex import regex

from grandpybot.chatbots.openmediawiki import OpenMediaWikiBot
from grandpybot.chatbots.openstreetmap import OpenStreetMapBot


class ChatBotFactory(metaclass=ABCMeta):

    @abstractmethod
    def build(self):
        """abstract"""

    def get_object(self) -> any:
        return self.build()


class OpenStreetMapBotFactory(ChatBotFactory):

    def __init__(self, question):
        self.question = question

    def parse_question(self) -> str:
        parse_result = regex.search("(?<=(adresse (du |de |d')|situe (le |la |les | ))).*?(?= \\?)", self.question)
        return parse_result[0]

    def build(self) -> OpenStreetMapBot:
        clean_question = self.parse_question()
        osm_object = self.perform_search(clean_question)

        display_name = osm_object["display_name"]

        latitude = osm_object["lat"]
        longitude = osm_object["lon"]

        house_number = None
        if "house_number" in osm_object["address"]:
            house_number = osm_object["address"]["house_number"]

        locality = None
        if "village" in osm_object["address"]:
            locality = osm_object["address"]["village"]
        elif "city" in osm_object["address"]:
            locality = osm_object["address"]["city"]

        road = osm_object["address"]["road"]

        postcode = osm_object["address"]["postcode"]

        return OpenStreetMapBot(display_name, latitude, longitude, house_number, road, locality, postcode)

    @staticmethod
    def perform_search(search_term):
        osm_response = requests.get("https://nominatim.openstreetmap.org/search?"
                                    f"q={search_term}&"
                                    "addressdetails=1&"
                                    "countrycodes=fr&"
                                    "limit=1&"
                                    "format=json")

        return osm_response.json()[0]


class OpenMediaWikiBotFactory(ChatBotFactory):

    def __init__(self, latitude, longitude):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude

    def build(self) -> OpenMediaWikiBot:
        omw_object = self.perform_geo_search(self.latitude, self.longitude)

        page_ids = []
        if "query" in omw_object and "geosearch" in omw_object["query"]:
            for item in omw_object["query"]["geosearch"]:
                page_ids.append(item["pageid"])

        random_index = random.randint(0, len(page_ids) - 1)
        chosen_page_id = page_ids[random_index]

        omw_object = self.perform_query_search(chosen_page_id)

        intro = omw_object["query"]["pages"][str(chosen_page_id)]["extract"]

        return OpenMediaWikiBot(intro)

    @staticmethod
    def perform_geo_search(latitude, longitude):
        omw_response = requests.get("https://fr.wikipedia.org/w/api.php?"
                                    "action=query&"
                                    "list=geosearch&"
                                    f"gscoord={latitude}|{longitude}&"
                                    "gsradius=10000&"  # 10 000 meters, so 10kms max around
                                    "gslimit=10&"  # 10 results max
                                    "format=json")

        return omw_response.json()

    @staticmethod
    def perform_query_search(chosen_page_id):
        omw_response = requests.get("https://fr.wikipedia.org/w/api.php?"
                                    "action=query&"
                                    "prop=extracts&"
                                    "explaintext&"
                                    "exsentences=3&"
                                    "exsectionformat=plain&"
                                    f"pageids={chosen_page_id}&"
                                    "format=json")

        return omw_response.json()
