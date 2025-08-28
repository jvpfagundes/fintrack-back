from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth import AuthService
from app.schemas.auth import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    auth_service = AuthService()
    phone_number = auth_service.verify_token(token)

    if phone_number is None:
        raise credentials_exception

    user = await auth_service.get_user(phone_number=phone_number)
    if user is None:
        raise credentials_exception

    return User(**user)


async def get_current_active_user(
        current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.status:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

