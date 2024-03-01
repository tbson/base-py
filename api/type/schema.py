from django_hint import StandardModelType

TenantSchema = StandardModelType["Tenant"]

UserSchema = StandardModelType["User"]
RoleSchema = StandardModelType["Role"]
PemSchema = StandardModelType["Pem"]


OtpSchema = StandardModelType["Otp"]
TrustedTargetSchema = StandardModelType["TrustedTarget"]

EmailLogSchema = StandardModelType["EmailLog"]
AuditLogSchema = StandardModelType["AuditLog"]

VariableSchema = StandardModelType["Variable"]
