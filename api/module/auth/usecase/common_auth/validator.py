from ninja import Schema


class RefreshTokenInput(Schema):
    refresh_token: str
