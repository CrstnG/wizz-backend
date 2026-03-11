from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import SignUpRequest
from app.utils.security import hash_password, verify_password, create_access_token


def register_user(db: Session, data: SignUpRequest) -> User:
    """
    Registra un nuevo usuario. Lanza ValueError si el email o username ya existen.
    """
    if db.query(User).filter(User.email == data.email).first():
        raise ValueError("El email ya está registrado")

    if db.query(User).filter(User.username == data.username).first():
        raise ValueError("El username ya está en uso")

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> str:
    """
    Verifica credenciales y retorna un JWT de acceso.
    Lanza ValueError si las credenciales son inválidas.
    """
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Credenciales inválidas")

    if not user.is_active:
        raise ValueError("Usuario inactivo")

    return create_access_token({"sub": user.email})
