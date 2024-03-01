from interface.config import VariableCrud
from module.config.const import VARIABLE_TYPE_CHOICE
from module.config.models import Variable
from ninja import Query
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import VariableSchema
from util.error_util import ErrorUtil


class VariableService(VariableCrud):
    def get_variable_list_with_filter(
        self, condition: Condition, order: str, filter: Query
    ) -> Result[QuerySet[VariableSchema]]:
        try:
            list_item = Variable.objects.filter(**condition).order_by(order)
            return filter.filter(list_item), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_type_option(self) -> list[dict]:
        return [{"value": item[0], "label": item[1]} for item in VARIABLE_TYPE_CHOICE]
