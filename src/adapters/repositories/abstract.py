import abc

from src.adapters import orm


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, note: orm.Note) -> None:
        raise NotImplementedError

    # @abc.abstractmethod
    # def add_all(self, note):
    #     raise NotImplementedError

    @abc.abstractmethod
    def get(self, oid: int) -> orm.Note:
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_by_sleep_date(self, sleep_date):
    #     raise NotImplementedError
