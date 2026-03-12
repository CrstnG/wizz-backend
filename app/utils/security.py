import hashlib
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Convierte una contraseña en texto plano a su hash bcrypt."""
    # Bcrypt only supports up to 72 bytes. Pre-hashing with sha256 fixes length limits.
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(hashed_pass)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña en texto plano contra su hash almacenado."""
    hashed_pass = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(hashed_pass, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Genera un JWT firmado que expira en ACCESS_TOKEN_EXPIRE_MINUTES minutos.
    El payload 'data' normalmente contiene {"sub": user_email}.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """
    Decodifica y valida un JWT. Retorna el payload si es válido, None si no.
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
