from src.chatbots.chatbotfactory import OpenStreetMapBotFactory
from src.chatbots.openstreetmap import OpenStreetMapBot


def test_get_answer():
    question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"
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
