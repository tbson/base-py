class VariableType:
    STRING = 1
    INTEGER = 2
    FLOAT = 3
    DATE = 4
    DATETIME = 5


VARIABLE_TYPE_CHOICE = (
    (VariableType.STRING, "String"),
    (VariableType.INTEGER, "Integer"),
    (VariableType.FLOAT, "Float"),
    (VariableType.DATE, "Date"),
    (VariableType.DATETIME, "Date time"),
)

VARIABLE_TYPE_DICT = dict(VARIABLE_TYPE_CHOICE)
