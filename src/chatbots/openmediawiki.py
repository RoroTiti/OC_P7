from src.chatbots.chatbot import ChatBot


class OpenMediaWikiBot(ChatBot):

    def __init__(self, intro):
        self.intro = intro

    def get_answer(self):
        base_answer = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? "
        base_answer += self.intro
        return base_answer
