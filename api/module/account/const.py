class ProfileType:
    ADMIN = 1
    STAFF = 30
    MANAGER = 60
    USER = 90


SYSTEM_PROFILE_TYPES = [
    ProfileType.ADMIN,
    ProfileType.STAFF,
]

TENANT_PROFILE_TYPES = [
    ProfileType.MANAGER,
    ProfileType.USER,
]

PROFILE_TYPE_CHOICE = (
    (ProfileType.ADMIN, "Admin"),
    (ProfileType.STAFF, "Staff"),
    (ProfileType.MANAGER, "Manager"),
    (ProfileType.USER, "User"),
)

PROFILE_TYPE_CHOICE_ADMIN = (
    (ProfileType.ADMIN, "Admin"),
    (ProfileType.STAFF, "Staff"),
)

PROFILE_TYPE_CHOICE_TENANT = (
    (ProfileType.MANAGER, "Manager"),
    (ProfileType.USER, "User"),
)

PROFILE_TYPE_DICT = dict(PROFILE_TYPE_CHOICE)
