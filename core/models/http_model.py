from core.models.field import Field


class HttpModel:

    def __init__(self, params: dict):
        self.params: dict = params

    def Field(self, data_type, alias: str, default=None):
        return Field(data_type, self.params.get(alias), alias=alias, default=default)
