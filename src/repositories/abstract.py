import abc

from src import orm


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, note: orm.Note) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, oid: int) -> orm.Note:
        raise NotImplementedError

    # def get_by_sleep_date(self, sleep_date):
    # def get_all(self):
    # def add_all(self, note):
    # def update(self):
    # def delete(self, oid):
    # def delete_all(self):
