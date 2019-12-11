from abc import ABC, abstractmethod


class ChatBot(ABC):
    """
    The Product interface declares the operations that all concrete products
    must implement.
    """

    @abstractmethod
    def operation(self) -> str:
        pass

    @abstractmethod
    def get_answer(self) -> str:
        pass
