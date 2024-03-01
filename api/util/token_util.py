from typing import Tuple, Union, cast
from uuid import uuid4

import jwt
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from type.general import Token
from type.result import Result
from util.date_util import DateUtil
from util.error_util import ErrorUtil

JWT_CONFIG = settings.JWT_CONFIG


class TokenType:
    ACCESS = "access"
    REFRESH = "refresh"


class TokenUtil:
    @staticmethod
    def get_token_from_headers(headers: dict, is_jwt: bool = True) -> str:
        prefix = "JWT " if is_jwt else "bearer "
        full_token = headers.get("Authorization")
        if not full_token:
            return ""
        token_arr = full_token.split(" ")
        if len(token_arr) != 2:
            return ""
        prefix = token_arr[0]
        token = token_arr[1]

        return "" if not token or prefix not in ["bearer", "JWT"] else token

    @staticmethod
    def get_token_signature(token: str) -> str:
        return token.split(".")[-1]

    @staticmethod
    def encode_access_token(user_id: str, pems: list[str]) -> str:
        """
        {
          "token_type": "access",
          "exp": 1695769432,
          "iat": 1695769132,
          "jti": "f3d9eb6ed76e433ba45bc045d39f7818",
          "user_id": 3
        }
        """
        return jwt.encode(
            {
                "token_type": TokenType.ACCESS,
                "exp": DateUtil.now(True) + JWT_CONFIG["ACCESS_TOKEN_LIFETIME"],
                "iat": DateUtil.now(True),
                "user_id": user_id,
                "jti": uuid4().hex,
                "pems": pems,
            },
            JWT_CONFIG["SECRET_KEY"],
            algorithm=JWT_CONFIG["ALGORITHM"],
        )

    @staticmethod
    def encode_refresh_token(user_id: str) -> str:
        """
        {
          "token_type": "refresh",
          "exp": 1695855532,
          "iat": 1695769132,
          "jti": "637c01b6e9ee4de8b78212bd381777c4",
          "user_id": 3
        }
        """
        return jwt.encode(
            {
                "token_type": TokenType.REFRESH,
                "exp": DateUtil.now(True) + JWT_CONFIG["REFRESH_TOKEN_LIFETIME"],
                "iat": DateUtil.now(True),
                "jti": uuid4().hex,
                "user_id": user_id,
            },
            JWT_CONFIG["SECRET_KEY"],
            algorithm=JWT_CONFIG["ALGORITHM"],
        )

    @staticmethod
    def decode(token: Token) -> Result[dict]:
        error_message = _("can not decode token")
        try:
            return (
                jwt.decode(
                    token,
                    JWT_CONFIG["SECRET_KEY"],
                    algorithms=[JWT_CONFIG["ALGORITHM"]],
                ),
                True,
            )
        except Exception as e:
            print(e)
            return (ErrorUtil.format(error_message), False)

    @staticmethod
    def is_access(token: Token) -> bool:
        clams, ok = TokenUtil.decode(token)
        return clams.get("token_type") == TokenType.ACCESS if ok else False

    @staticmethod
    def is_refresh(token: Token) -> bool:
        clams, ok = TokenUtil.decode(token)
        return clams.get("token_type") == TokenType.REFRESH if ok else False

    @staticmethod
    def get_id(token: Token) -> Union[int, None]:
        clams, ok = TokenUtil.decode(token)
        if not ok:
            return None
        user_id = cast(str, clams.get("user_id"))
        return int(user_id) if user_id else None

    @staticmethod
    def refresh_token(token: Token) -> Result[Tuple[Token, Token]]:
        error_message = _("can not refresh token")
        (result, ok) = TokenUtil.decode(token)
        if not ok:
            return (ErrorUtil.format(error_message), False)
        decoded = cast(dict, result)

        token_type = decoded.get("token_type")
        if token_type != TokenType.REFRESH:
            return (ErrorUtil.format(error_message), False)
        user_id = str(decoded.get("user_id"))
        pems = cast(list[str], decoded.get("pems"))
        access_token = TokenUtil.encode_access_token(user_id, pems)
        refresh_token = TokenUtil.encode_refresh_token(user_id)
        return ((access_token, refresh_token), True)
