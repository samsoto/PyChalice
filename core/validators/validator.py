from core.models.field import Field


def validate_is_valid(field: Field):
    if ~field.is_valid:
        raise Exception('')


def validate_id(field: Field):
    validate_is_valid(field)
    if field.data_type is not int:
        raise Exception('')
