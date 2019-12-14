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
        determinants = ["le", "la", "l", "les", "de", "du", "d"]
        verbs = ["situe", "situent", "adresse"]

        self.question = self.question.replace("'", " ")

        words_list = self.question.split(" ")

        verb_index = 0
        for verb in verbs:
            if verb in words_list:
                verb_index = words_list.index(verb)
                break

        if words_list[verb_index + 1] in determinants:
            words_list.pop(verb_index + 1)

        self.question = " ".join(words_list)

        words_list = self.question.split(" ")

        search_term = ""
        start_index = 0
        end_index = 0

        for verb in verbs:
            if verb in self.question:
                for i in range(0, len(words_list)):
                    if verb in words_list[i]:
                        start_index = i + 1
                    elif words_list[i] == "?":
                        end_index = i
                        break

        for i in range(start_index, end_index):
            search_term += words_list[i] + " "

        return search_term.rstrip()

    def build(self) -> OpenStreetMapBot:
        clean_question = self.parse_question()
        osm_object = self.perform_search(clean_question)

        display_name = osm_object["display_name"]
        latitude = osm_object["lat"]
        longitude = osm_object["lon"]

        return OpenStreetMapBot(display_name, latitude, longitude)

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
                                    "exsentences=3&"
                                    f"pageids={chosen_page_id}&"
                                    "format=json")

        return omw_response.json()
