from __future__ import annotations

from abc import abstractmethod, ABCMeta

from regex import regex

from src.chatbots.openmediawiki import OpenMediaWikiBot
from src.chatbots.openstreetmap import OpenStreetMapBot


class ChatBotFactory(metaclass=ABCMeta):
    def __init__(self, question):
        self.question = question

    @abstractmethod
    def build(self):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        pass

    def get_object(self) -> str:
        """
        Also note that, despite its name, the Creator's primary responsibility
        is not creating products. Usually, it contains some core business logic
        that relies on Product objects, returned by the factory method.
        Subclasses can indirectly change that business logic by overriding the
        factory method and returning a different type of product from it.
        """
        # Call the factory method to create a Product object.
        result = self.build()
        # Now, use the product.
        # result = f"Creator: The same creator's code has just worked with {product.operation()}"
        return result

    def parse_question(self) -> str:
        parse_result = regex.search("(?<=(adresse (du |de |d')|situe (le |la |les | ))).*?(?= \\?)", self.question)
        return parse_result[0]


class OpenStreetMapBotFactory(ChatBotFactory):
    def build(self) -> OpenStreetMapBot:
        clean_question = super().parse_question()
        return OpenStreetMapBot()


class OpenMediaWikiBotFactory(ChatBotFactory):
    def build(self) -> OpenMediaWikiBot:
        clean_question = super().parse_question()
        return OpenMediaWikiBot(clean_question)
