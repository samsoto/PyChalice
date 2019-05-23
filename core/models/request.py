from core.validators import validator
from core.models.http_model import HttpModel
from core.models.field import Field


def FieldBuilder(params: dict):
    def field(data_type, alias: str, default=None) -> Field:
        return Field(data_type, params.get(alias), alias=alias, default=default)
    return field


class Request:

    def __init__(self, params: dict):
        field = FieldBuilder(params)
        self.id = field(int, 'id')
        self.order_by = field(str, 'orderBy', default='time')
        self.offset = field(int, 'offset', default=0)
        self.limit = field(int, 'limit', default=10)

    def validate(self):
        validator.validate_id(self.id)


