from typing import Optional

from django.utils.translation import gettext_lazy as _
from interface.config import Config
from module.config.models import Variable
from type.general import Condition, QuerySet
from type.result import Result
from type.schema import VariableSchema
from util.error_util import ErrorUtil
from util.framework.schema_util import SchemaUtil


class ConfigService(Config):
    def get_list_variable(
        self, condition: Condition, limit: Optional[int] = None, order_by: str = "-id"
    ) -> Result[QuerySet[VariableSchema]]:
        try:
            query = Variable.objects.filter(**condition).order_by(order_by)
            if limit is not None:
                query = query[:limit]
            return query, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_variable(self, condition: Condition) -> Result[VariableSchema]:
        try:
            return Variable.objects.get(**condition), True
        except Variable.DoesNotExist:
            err_msg = _("variable does not exist")
            return ErrorUtil.format(err_msg), False

    def create_variable(self, condition: Condition) -> Result[VariableSchema]:
        try:
            return Variable.objects.create(**condition), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def update_variable(
        self, condition: Condition, data: dict
    ) -> Result[VariableSchema]:
        result, ok = self.get_variable(condition)
        if not ok:
            return result, False
        variable = result
        return SchemaUtil.update(variable, data)

    def delete_variable(self, condition: Condition) -> Result[list[int]]:
        try:
            variables = Variable.objects.filter(**condition)
            variables.delete()
            return list(variables.values_list("id", flat=True)), True
        except Exception as e:
            return ErrorUtil.format(e), False
