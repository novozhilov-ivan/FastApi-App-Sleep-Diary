from datetime import datetime, timedelta

import bcrypt
import jwt

from api import config


def encode_jwt(
    payload: dict,
    private_key: str = config.auth_jwt.private_key_path.read_text(),
    algorithm: str = config.auth_jwt.algorithm,
    expire_minutes: int = config.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    utc_now = datetime.utcnow()
    if expire_timedelta:
        expire = utc_now + expire_timedelta
    else:
        expire = utc_now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=utc_now,
    )
    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )


def decode_jwt(
    payload: str | bytes,
    public_key: str = config.auth_jwt.public_key_path.read_text(),
    algorithm: str = config.auth_jwt.algorithm,
):
    return jwt.decode(
        payload,
        public_key,
        algorithms=[algorithm],
    )


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: bytes,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password,
        hashed_password=hashed_password,
    )
