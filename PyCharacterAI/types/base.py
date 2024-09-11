class BaseCAI:
    def __init__(self, options: dict):
        self.__raw = options

    def get_dict(self, raw: bool = False):
        fields = self.__dict__.copy()
        fields.pop("_BaseCAI__raw")
        
        if raw:
            return self.__raw
        return fields


