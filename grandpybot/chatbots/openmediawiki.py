from grandpybot.chatbots.chatbot import ChatBot


class OpenMediaWikiBot(ChatBot):
    """
    Concrete implementation of a chat bot with OpenMediaWiki features
    """

    def __init__(self, intro):
        """
        Initializes an OpenMediaWikiChatBot object
        """
        self.intro = intro

    def get_answer(self):
        """
        Return the answer according to fetched API results
        """
        base_answer = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? "
        base_answer += self.intro
        return base_answer
