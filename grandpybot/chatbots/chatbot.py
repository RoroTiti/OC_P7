from abc import abstractmethod, ABCMeta


class ChatBot(metaclass=ABCMeta):
    """
    Abstract class acting as a framework for any chat bot offered by the app
    """

    @abstractmethod
    def get_answer(self) -> str:
        """
        Allow to obtain the answer shown in the web app from any chat bot
        """
