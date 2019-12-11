from src.chatbots.chatbot import ChatBot


class OpenStreetMapBot(ChatBot):

    def __init__(self, display_name, latitude, longitude, house_number, road, locality, postcode):
        self.display_name = display_name
        self.latitude = latitude
        self.longitude = longitude
        self.house_number = house_number
        self.road = road
        self.locality = locality
        self.postcode = postcode

    def get_answer(self):
        base_answer = "Bien sûr mon poussin ! La voici : "
        if self.house_number is not None:
            base_answer += f"{self.house_number} "
        base_answer += f"{self.road}, {self.postcode} {self.locality}."
        return base_answer
