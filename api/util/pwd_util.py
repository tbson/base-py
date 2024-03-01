from django.contrib.auth.hashers import check_password, make_password


class PwdUtil:
    @staticmethod
    def make_password(raw_password: str) -> str:
        return make_password(raw_password)

    @staticmethod
    def check_password(raw_password: str, hash_password: str) -> bool:
        return check_password(raw_password, hash_password)
