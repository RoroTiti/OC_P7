from __future__ import annotations

from abc import abstractmethod, ABCMeta

import requests
from regex import regex

from src.chatbots.openmediawiki import OpenMediaWikiBot
from src.chatbots.openstreetmap import OpenStreetMapBot


class ChatBotFactory(metaclass=ABCMeta):
    def __init__(self, question):
        self.question = question

    @abstractmethod
    def build(self):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        pass

    def get_object(self) -> any:
        """
        Also note that, despite its name, the Creator's primary responsibility
        is not creating products. Usually, it contains some core business logic
        that relies on Product objects, returned by the factory method.
        Subclasses can indirectly change that business logic by overriding the
        factory method and returning a different type of product from it.
        """
        # Call the factory method to create a Product object.
        result = self.build()
        # Now, use the product.
        # result = f"Creator: The same creator's code has just worked with {product.operation()}"
        return result

    def parse_question(self) -> str:
        parse_result = regex.search("(?<=(adresse (du |de |d')|situe (le |la |les | ))).*?(?= \\?)", self.question)
        return parse_result[0]


class OpenStreetMapBotFactory(ChatBotFactory):
    def build(self) -> OpenStreetMapBot:
        clean_question = super().parse_question()

        osm_response = requests.get("https://nominatim.openstreetmap.org/search?"
                                    f"q={clean_question}&"
                                    "addressdetails=1&"
                                    "countrycodes=fr&"
                                    "limit=1&"
                                    "format=json")

        osm_object = osm_response.json()[0]

        display_name = osm_object["display_name"]

        latitude = osm_object["lat"]
        longitude = osm_object["lon"]

        house_number = None
        if osm_object["address"]["house_number"]:
            house_number = osm_object["address"]["house_number"]

        locality = None
        if "village" in osm_object["address"]:
            locality = osm_object["address"]["village"]
        elif "city" in osm_object["address"]:
            locality = osm_object["address"]["city"]

        road = osm_object["address"]["road"]

        postcode = osm_object["address"]["postcode"]

        return OpenStreetMapBot(display_name, latitude, longitude, house_number, road, locality, postcode)


class OpenMediaWikiBotFactory(ChatBotFactory):
    def build(self) -> OpenMediaWikiBot:
        clean_question = super().parse_question()
        return OpenMediaWikiBot()
