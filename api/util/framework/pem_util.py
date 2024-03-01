class PemUtil:
    @staticmethod
    def format_pem_codename(module: str, action: str) -> str:
        action_map = {
            "get_list": "view",
            "get_item": "view",
            "create": "add",
            "update": "change",
            "delete_list": "delete",
        }
        return f"{action_map.get(action, action)}_{module}"
