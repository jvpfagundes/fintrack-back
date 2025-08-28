from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from app.schemas.auth import User
from app.core.auth import get_current_user
from app.services.expenses import Expenses
from app.schemas.expenses import  ExpenseCreate
router = APIRouter()


@router.get("/categories")
async def get_user_categories(user_id: str = Query(None, alias='user_id'),
                      current_user: User = Depends(get_current_user)):
    user_id = user_id

    response = await Expenses(user_id).get_categories()

    return JSONResponse(content=response, status_code=response['status_code'])


@router.post('/')
async def create_expense(expense_data: ExpenseCreate,
                         current_user: User = Depends(get_current_user)):
    user_id = expense_data.user_id
    response = await Expenses(user_id).create_expense(from_type='n8n', payload=expense_data)

    return JSONResponse(content=response, status_code=response['status_code'])


@router.get('/cards')
async def get_expenses_cards(current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    response = await Expenses(user_id).get_cards()

    return JSONResponse(content=response, status_code=response['status_code'])

@router.get('/table')
async def get_expenses_table(current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    response = await Expenses(user_id).get_table()

    return JSONResponse(content=response, status_code=response['status_code'])

@router.get('/graphic/categories')
async def get_categories_graphic(current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    response = await Expenses(user_id).get_categories_graphic()
    return JSONResponse(content=response, status_code=response['status_code'])

@router.get('/graphic/days')
async def get_days_graphic(current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    response = await Expenses(user_id).get_days_graphic()
    return JSONResponse(content=response, status_code=response['status_code'])
