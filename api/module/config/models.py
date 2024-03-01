from django.db import models
from module.config.const import VARIABLE_TYPE_CHOICE, VARIABLE_TYPE_DICT, VariableType
from contract.type.schema import VariableSchema


class Variable(models.Model, VariableSchema):
    uid = models.CharField(max_length=255, unique=True)
    value = models.TextField(null=False, blank=True, default="")
    description = models.TextField(null=False, blank=True, default="")
    type = models.PositiveSmallIntegerField(
        choices=VARIABLE_TYPE_CHOICE, default=VariableType.STRING
    )

    @property
    def type_label(self) -> str:
        return VARIABLE_TYPE_DICT.get(self.type, "Unknown")

    def __str__(self) -> str:
        return f"{self.uid} - {self.value}"

    class Meta:
        db_table = "variables"
        ordering = ["-id"]
