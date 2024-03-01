class AuditLogType:
    SIGNUP = 1
    LOGIN = 2
    LOGOUT = 3
    CHANGE_PWD = 4
    RESET_PWD = 5
    REFRESH_TOKEN = 6


SECURITY_LOG_TYPE_CHOICE = (
    (AuditLogType.SIGNUP, "Signup"),
    (AuditLogType.LOGIN, "Login"),
    (AuditLogType.LOGOUT, "Logout"),
    (AuditLogType.CHANGE_PWD, "Change password"),
    (AuditLogType.RESET_PWD, "Reset password"),
    (AuditLogType.REFRESH_TOKEN, "Refresh token"),
)
