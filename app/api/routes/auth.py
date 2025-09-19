from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from app.core.auth import get_current_user
from app.schemas.auth import Token, LoginSchema, User, UserCreate
from app.services.auth import AuthService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login", response_model=Token)
async def login(
        form_data: LoginSchema):
    auth_service = AuthService()
    user = await auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorret Credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(data={
        "phone_number": user["phone_number"],
        "birth_date": str(user["birth_date"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "is_first_access": user["is_first_access"],
        "monthly_goal": user["monthly_goal"],
        "daily_goal": user["daily_goal"],
        "theme": user["theme"],
        "language": user["language"]

    })
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/get_user_id')
async def get_user_id(phone_number: str = Query(None, alias='phone_number'),
                      current_user: User = Depends(get_current_user)):

    response = await AuthService().get_user(phone_number=phone_number)


    return {'user_id': response['id'] if response else '', 'status': True, 'status_code': 200}



@router.post("/register")
async def register(
    user_data: UserCreate):
    try:
        auth_service = AuthService()

        response = await auth_service.register_user(user_data)

        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )