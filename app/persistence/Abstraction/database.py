from abc import ABC, abstractmethod


class database(ABC):
    @abstractmethod
    def get_connection_string(self):
        pass

    @abstractmethod
    def __init__(self, connection_string: str = None):
        if connection_string:
            self._connection_string = connection_string
        else:
            self._connection_string = self.get_connection_string()
