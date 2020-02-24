from grandpybot.main import parse_question


def test_parser():
    question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"
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

    question = "Salut GrandPy ! Peux-tu me dire où se trouve le Puy du Fou ?"
    parse_result = parse_question(question)
    assert parse_result == "Puy du Fou"

    question = "Salut GrandPy ! Peux-tu me dire où le Futuroscope est-il situé ?"
    parse_result = parse_question(question)
    assert parse_result == "Futuroscope"

    question = "Salut GrandPy ! J'aimerais voir la rue des têtes ?"
    parse_result = parse_question(question)
    assert parse_result == "rue des têtes"

    question = "Salut GrandPy ! J'aimerais aller à la Grande Roue à Paris ?"
    parse_result = parse_question(question)
    assert parse_result == "Grande Roue à Paris"
