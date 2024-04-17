class NotFoundError(Exception):
    @property
    def message(self):
        return "NOT FOUND"
