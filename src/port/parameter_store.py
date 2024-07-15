from abc import ABC, abstractmethod


class ParameterStore(ABC):
    @abstractmethod
    def get_parameter(self, name: str):
        raise NotImplementedError
