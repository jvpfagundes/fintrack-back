from app.core.sql_async import SQLQueryAsync
from app.schemas.expenses import ExpenseCreate
from app.services.decorator import Response
from app.utils.date import str_to_date, str_to_time

class Expenses(SQLQueryAsync):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id

    @Response(desc_error="Error creating expense", return_list=[])
    async def create_expense(self, from_type: str, payload: ExpenseCreate):
        dict_insert: dict = {
            'user_id': payload.user_id,
            'expense_date': str_to_date(expense_date=payload.date),
            'expense_time': str_to_time(expense_time=payload.time),
            'amount': payload.amount,
            'category_id': payload.category_id,
        }
        expense_id: int = await self.insert('expenses', dict_insert=dict_insert)

        return expense_id

    @Response(desc_error="Error fetching categories.", return_list=["categories_list"])
    async def get_categories(self):
        return await self.select("""
        select id::varchar, name from public.expense_category 
        where status = true and (user_id isnull or user_id = :user_id)
        """, parameters=dict(user_id=self.user_id))


    @Response(desc_error="Error fetching cards.", return_list=["cards_dict"])
    async def get_cards(self):
        return await self.select(f"""
        SELECT 
            (SELECT c.name
             FROM expenses e
             join public.expense_category c
                on c.id = e.category_id
              where e.status = true 
                    and c.status = true 
             GROUP BY c.id
             ORDER BY SUM(amount) DESC
             LIMIT 1) AS top_category,
            SUM(amount)::float AS total_expenses,
            count(id) as last_transactions
        FROM expenses
        where user_id = :user_id
              and status = true;
        """, parameters=dict(user_id=self.user_id), is_first=True)


    @Response(desc_error="Error fetching table.", return_list=["expenses_list"])
    async def get_table(self):
        return await self.select(f"""
        select to_char(e.expense_date, 'dd/mm/yyyy') as expense_date,
               e.amount::float as value,
               c.name as category_name
        from expenses e 
        join expense_category c 
            on c.id = e.category_id
        where e.status = true 
              and e.user_id = :user_id;
        """, parameters=dict(user_id=self.user_id))

    @Response(desc_error="Error fetching categories graphic.", return_list=['categories_list'])
    async def get_categories_graphic(self):
        ls_categories = await self.select(f"""
        select c.name,
               sum(e.amount)::float as value
        from expenses e 
        join expense_category c 
            on c.id = e.category_id
        where e.status = true 
              and c.status = true 
              and e.user_id = :user_id
        group by c.name;
        """, parameters=dict(user_id=self.user_id)) or []
        total = sum(i['value'] for i in ls_categories)
        for i in ls_categories:
            i['perc'] = round(i['value'] / total * 100, 2)
        return ls_categories


    @Response(desc_error="Error fetching days graphic.", return_list=['days_list'])
    async def get_days_graphic(self):
        return await self.select(f"""
        select extract(day from e.expense_date)::integer as day,
               sum(e.amount)::float as value
        from expenses e
        where e.status = true
        and e.user_id = :user_id
        group by e.expense_date;
        """, parameters=dict(user_id=self.user_id))