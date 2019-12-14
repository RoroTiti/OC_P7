from grandpybot.chatbots.chatbot import ChatBot


class OpenStreetMapBot(ChatBot):

    def __init__(self, display_name, latitude, longitude):
        self.display_name = display_name
        self.latitude = latitude
        self.longitude = longitude

    def get_answer(self):
        return f"Bien sûr mon poussin ! La voici : {self.display_name}"
