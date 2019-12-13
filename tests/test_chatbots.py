import random

import requests

from grandpybot.chatbots.chatbotfactory import OpenMediaWikiBotFactory, OpenStreetMapBotFactory
from grandpybot.chatbots.openmediawiki import OpenMediaWikiBot
from grandpybot.chatbots.openstreetmap import OpenStreetMapBot


def test_chatbots(monkeypatch):
    question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"

    # Any arguments may be passed and mock_get_osm() will always return our
    # mocked object, which only has the .json() method.
    def mock_get_osm(*args, **kwargs):
        return OSMMockResponse()

    def mock_get_osm_search(*args, **kwargs):
        return OSMMockResponse().perform_search()

    def mock_get_omw_geo_search(*args, **kwargs):
        return OMWMockResponse().perform_geo_search()

    def mock_get_omw_query_search(*args, **kwargs):
        return OMWMockResponse().perform_query_search()

    def mock_get_randint(*args, **kwargs):
        return RandomMockResponse().randint()

    # apply the monkeypatch for requests.get to mock_get_osm
    monkeypatch.setattr(OpenStreetMapBotFactory, "perform_search", mock_get_osm_search)

    factory = OpenStreetMapBotFactory(question)
    osm: OpenStreetMapBot = factory.get_object()

    assert osm.get_answer() == "Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris."
    assert osm.display_name == "OpenClassRooms, " \
                               "7, Cité Paradis, " \
                               "Quartier de la Porte-Saint-Denis, " \
                               "Paris 10e Arrondissement, " \
                               "Paris, Île-de-France, " \
                               "France métropolitaine, " \
                               "75010, " \
                               "France"
    assert osm.latitude == "48.8747786"
    assert osm.longitude == "2.3504885"

    factory = OpenMediaWikiBotFactory(osm.latitude, osm.longitude)

    # apply the monkeypatch for requests.get to mock_get_osm
    monkeypatch.setattr(OpenMediaWikiBotFactory, "perform_geo_search", mock_get_omw_geo_search)
    monkeypatch.setattr(OpenMediaWikiBotFactory, "perform_query_search", mock_get_omw_query_search)
    monkeypatch.setattr(random, "randint", mock_get_randint)

    omw: OpenMediaWikiBot = factory.get_object()

    assert omw.intro == "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris.\n\n\nSituation et accès\nLa " \
                        "cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, " \
                        "une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse. "

    assert omw.get_answer() == "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? " + omw.intro

    # delete the monkeypatch for requests.get
    monkeypatch.delattr(requests, "get")


# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class OSMMockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def perform_search():
        return {
            "place_id": 251835758,
            "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
            "osm_type": "node",
            "osm_id": 6242758322,
            "boundingbox": [
                "48.8747286",
                "48.8748286",
                "2.3504385",
                "2.3505385"
            ],
            "lat": "48.8747786",
            "lon": "2.3504885",
            "display_name": "OpenClassRooms, 7, Cité Paradis, Quartier de la Porte-Saint-Denis, Paris 10e Arrondissement, Paris, Île-de-France, "
                            "France métropolitaine, 75010, France",
            "class": "office",
            "type": "company",
            "importance": 0.101,
            "address": {
                "address29": "OpenClassRooms",
                "house_number": "7",
                "road": "Cité Paradis",
                "suburb": "Quartier de la Porte-Saint-Denis",
                "city_district": "Paris 10e Arrondissement",
                "city": "Paris",
                "county": "Paris",
                "state": "Île-de-France",
                "country": "France",
                "postcode": "75010",
                "country_code": "fr"
            }
        }


class OMWMockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def perform_geo_search():
        return {
            "batchcomplete": "",
            "query": {
                "geosearch": [
                    {
                        "pageid": 5653202,
                        "ns": 0,
                        "title": "Cité Paradis",
                        "lat": 48.87409,
                        "lon": 2.35064,
                        "dist": 77.4,
                        "primary": ""
                    },
                ]
            }
        }

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def perform_query_search():
        return {
            "batchcomplete": "",
            "warnings": {
                "extracts": {
                    "*": "\"exlimit\" was too large for a whole article extracts request, lowered to 1."
                }
            },
            "query": {
                "pages": {
                    "5653202": {
                        "pageid": 5653202,
                        "ns": 0,
                        "title": "Cité Paradis",
                        "extract": "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris.\n\n\nSituation et accès\nLa "
                                   "cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, "
                                   "une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse. "
                    }
                }
            }
        }


class RandomMockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def randint():
        return 0
