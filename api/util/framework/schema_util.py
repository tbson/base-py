from type.general import QuerySetObj
from type.result import Result
from util.error_util import ErrorUtil


class SchemaUtil:
    @staticmethod
    def update(schema: QuerySetObj, data: dict) -> Result[QuerySetObj]:
        try:
            for key, value in data.items():
                setattr(schema, key, value)
            schema.save()
            return schema, True
        except Exception as e:
            return ErrorUtil.format(e), False
