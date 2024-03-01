class MapUtil:
    @staticmethod
    def mask_password_related(data: dict) -> dict:
        result = data.copy()
        for key in result:
            if "password" in key or "pwd" in key:
                result[key] = "********"
        return result
