from abc import ABC, abstractmethod

class ClauseRetriever(ABC):

    @abstractmethod
    def retrieve(self, user_query: str):
        pass
