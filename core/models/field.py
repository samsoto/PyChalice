
class Field:

    def __init__(self, data_type, raw_value: str, alias: str, default=None):
        self.data_type = data_type
        self.raw_value = raw_value or default
        self.alias = alias
        self.is_valid = None
        self.value = None
        self.has_value = False
        try:
            self.value = self.data_type(self.raw_value)
            self.is_valid = True
            self.has_value = True
        except ValueError:
            self.value = None
            self.is_valid = False
            self.has_value = False
