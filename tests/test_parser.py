from grandpybot.chatbots.chatbotfactory import OpenStreetMapBotFactory


def test_parser():
    question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ? Et celle du Futuroscope ?"
    parse_result = OpenStreetMapBotFactory(question).parse_question()
    assert parse_result == "OpenClassrooms"

    question = "Salut GrandPy ! où se situe le OpenClassrooms ?"
    parse_result = OpenStreetMapBotFactory(question).parse_question()
    assert parse_result == "OpenClassrooms"

    question = "Salut GrandPy ! où se situe le Futuroscope ?"
    parse_result = OpenStreetMapBotFactory(question).parse_question()
    assert parse_result == "Futuroscope"

    question = "Salut GrandPy ! où se situe le Puy du Fou ?"
    parse_result = OpenStreetMapBotFactory(question).parse_question()
    assert parse_result == "Puy du Fou"
