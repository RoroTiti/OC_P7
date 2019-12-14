from grandpybot.chatbots.chatbotfactory import OpenStreetMapBotFactory
from grandpybot.main import parse_question


def test_parser():
    question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ? Et celle du Futuroscope ?"
    parse_result = parse_question(question)
    assert parse_result == "OpenClassrooms"

    question = "Salut GrandPy ! où se situe OpenClassrooms ?"
    parse_result = parse_question(question)
    assert parse_result == "OpenClassrooms"

    question = "Salut GrandPy ! où se situe le Futuroscope ?"
    parse_result = parse_question(question)
    assert parse_result == "Futuroscope"

    question = "Salut GrandPy ! où se situe le Puy du Fou ?"
    parse_result = parse_question(question)
    assert parse_result == "Puy du Fou"
