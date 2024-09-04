from abc import ABC, abstractmethod
import os


class database(ABC):
    @abstractmethod
    def get_connection_string(self, async_mode):
        pass