from src.chatbots.chatbot import ChatBot


class OpenStreetMapBot(ChatBot):

    def __init__(self, display_name, latitude, longitude):
        self.display_name = display_name
        self.latitude = latitude
        self.longitude = longitude

    def operation(self) -> str:
        return "{Result of the ConcreteProduct2}"

    def get_answer(self):
        pass
