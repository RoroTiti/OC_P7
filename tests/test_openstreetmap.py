from src.chatbot.openstreetmap import OpenStreetMap


def test_get_answer():
    osm = OpenStreetMap()
    question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"
    assert osm.get_answer(question) == "Bien sûr mon poussin ! La voici : 7 cité Paradis, 75010 Paris."

    question = "Salut GrandPy ! Est-ce que tu connais l'adresse du Futuroscope ?"
    assert osm.get_answer(question) == "Bien sûr mon poussin ! La voici : D 20d, 86360 Chasseneuil-du-Poitou."

    question = "Salut GrandPy ! Est-ce que tu connais l'adresse du Puy du Fou ?"
    assert osm.get_answer(question) == "Bien sûr mon poussin ! La voici : La Glaneuse, 85590 Les Épesses."
