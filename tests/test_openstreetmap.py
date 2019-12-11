from src.chatbots.chatbotfactory import OpenStreetMapBotFactory, OpenMediaWikiBotFactory


def test_get_answer():
    print("App: Launched with the ConcreteCreator1.")
    print(OpenStreetMapBotFactory().get_object())
    print("\n")

    print("App: Launched with the ConcreteCreator2.")
    print(OpenMediaWikiBotFactory().get_object())

    # question = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"
    # factory = ChatBotFactory(question)
    # factory.parse_question()
    # osm = factory.build_openstreetmap_bot()
    #
    # assert osm.get_answer() == "Bien sûr mon poussin ! La voici : 7 cité Paradis, 75010 Paris."
    # assert osm.display_name == "OpenClassRooms, " \
    #                            "7, Cité Paradis, " \
    #                            "Quartier de la Porte-Saint-Denis, " \
    #                            "Paris 10e Arrondissement, " \
    #                            "Paris, Île-de-France, " \
    #                            "France métropolitaine, " \
    #                            "75010, " \
    #                            "France"
    # assert osm.latitude == "48.8747786"
    # assert osm.longitude == "2.3504885"
