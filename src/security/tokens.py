from datetime import timedelta, datetime
from typing import Optional

from jose import jwt

from src.core.config import Settings


class UserTokens:
    """Class for realize creating access JWT."""
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Func for create JWT from something users data and secret key."""
        to_encode_data = data.copy()
        # if set time expire than add delta to now time
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode_data.update({"exp": expire})
        encoded_jwt = jwt.encode(claims=to_encode_data, key=Settings().SECRET_KEY, algorithm=Settings().ALGORITHM_HASH)
        return encoded_jwt
