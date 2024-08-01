import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, note):
        raise NotImplementedError

    @abc.abstractmethod
    def add_all(self, note):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, oid):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_sleep_date(self, sleep_date):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    ...  # fmt: skip
