from abc import ABC, abstractmethod


class ChatBot(ABC):

    @abstractmethod
    def get_answer(self) -> str:
        """abstract"""
