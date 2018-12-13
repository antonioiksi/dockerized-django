from abc import ABC, abstractmethod


class IComparator(ABC):

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def compare(first, second) -> bool:
        pass

    @staticmethod
    def implementations() -> list:
        return [{"name": cls.name, "title": cls.title, "method": cls.compare}
                for cls in IComparator.__subclasses__()]
