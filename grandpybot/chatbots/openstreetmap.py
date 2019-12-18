from grandpybot.chatbots.chatbot import ChatBot


class OpenStreetMapBot(ChatBot):
    """
    Concrete implementation of a chat bot with OpenMediaWiki features
    """

    def __init__(self, display_name, latitude, longitude):
        """
        Initializes an OpenStreetMapBot object
        """
        self.display_name = display_name
        self.latitude = latitude
        self.longitude = longitude

    def get_answer(self):
        """
        Return the answer according to fetched API results
        """
        return f"Bien sûr mon poussin ! La voici : {self.display_name}"
