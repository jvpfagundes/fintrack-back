from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from app.schemas.auth import User
from app.core.auth import get_current_user
from app.services.expenses import Expenses
from app.schemas.expenses import  ExpenseCreate, ExpenseDelete
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
    user_id = expense_data.user_id or current_user.id
    response = await Expenses(user_id).create_expense(from_type='n8n', payload=expense_data)

    return JSONResponse(content=response, status_code=response['status_code'])


@router.delete('/')
async def soft_delete_expense(expense_id: ExpenseDelete,
                              current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    response = await Expenses(user_id, expense_id.id).soft_delete_expense()

    return JSONResponse(content=response, status_code=response['status_code'])


@router.get('/cards')
async def get_expenses_cards(dat_start: str | None = Query(None), dat_end: str | None = Query(None), current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    response = await Expenses(user_id).get_cards(dat_start=dat_start, dat_end=dat_end)

    return JSONResponse(content=response, status_code=response['status_code'])

@router.get('/table')
async def get_expenses_table(dat_start: str | None = Query(None), dat_end: str | None = Query(None), current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    response = await Expenses(user_id).get_table(dat_start=dat_start, dat_end=dat_end)

    return JSONResponse(content=response, status_code=response['status_code'])

@router.get('/graphic/categories')
async def get_categories_graphic(dat_start: str | None = Query(None), dat_end: str | None = Query(None), current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    response = await Expenses(user_id).get_categories_graphic(dat_start=dat_start, dat_end=dat_end)
    return JSONResponse(content=response, status_code=response['status_code'])

@router.get('/graphic/days')
async def get_days_graphic(dat_start: str | None = Query(None), dat_end: str | None = Query(None), current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    response = await Expenses(user_id).get_days_graphic(dat_start=dat_start, dat_end=dat_end)
    return JSONResponse(content=response, status_code=response['status_code'])
