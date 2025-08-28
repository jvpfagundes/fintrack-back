from sqlalchemy import text
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from app.db.session import AsyncSessionLocal



class SQLQueryAsync:
    def __init__(self):
        pass


    @staticmethod
    def parse_list_to_tuple(parameters: Dict[str, Any]) -> None:
        for p in parameters:
            if isinstance(parameters[p], (list, set)):
                parameters[p] = tuple(parameters[p]) if parameters[p] else (None,)
            elif isinstance(parameters[p], tuple) and len(parameters[p]) == 0:
                parameters[p] = (None,)



    async def __query(self, query: str, parameters: Optional[Dict[str, Any]] = None, is_serialized: bool = True,
                      is_commit: bool = False) -> Optional[List[Dict[str, Any]]]:
        if parameters is None:
            parameters = {}
        self.parse_list_to_tuple(parameters)

        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(text(query), parameters)
                if not is_commit:
                    rows = result.fetchall()
                    return [dict(row._mapping) for row in rows] if is_serialized else list(rows)
                else:
                    await session.commit()
                    return None
            except Exception as e:
                print(e)
                await session.rollback()
                raise e



    @staticmethod
    def format_result(result: Optional[List[Dict[str, Any]]], is_values_list: bool = False, is_first: bool = False) -> Union[Dict[str, Any], List[Any], Any]:
        if not result:
            return {} if is_first else []

        if is_values_list:
            return_list = []
            for row in result:
                values = tuple(row.values())
                return_list.append(values[0] if len(values) == 1 else values)
            result = return_list

        return result[0] if is_first else result



    async def select(self, query: str, parameters: Dict[str, Any] = {}, is_values_list: bool = False, is_first: bool = False) -> Union[Dict[str, Any], List[Any], Any]:
        result = await self.__query(query=query, parameters=parameters, is_serialized=True)
        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)



    def __build_log(self, dict_object: Dict[str, Any], log_type: str) -> Dict[str, Any]:
        mapper_dict = {
            'save': 'updated_at',
            'insert': 'created_at',
            'update': 'updated_at',
            'delete': 'deleted_at',
        }
        log_col = mapper_dict[log_type]
        if log_col == 'updated_at' and 'id' not in dict_object:
            log_col = 'created_at'

        dict_object.setdefault('status', log_type != 'delete')
        dict_object[log_col] = datetime.utcnow()
        return dict_object



    async def update(self, table_name: str, dict_update: Dict[str, Any], dict_filter: Dict[str, Any],
                    pk_name: str = 'id', is_disable: bool = False, is_values_list: bool = False,
                    is_first: bool = True) -> Union[Dict[str, Any], List[Any], Any]:


        dict_update = self.__build_log(dict_update, 'update' if not is_disable else 'delete')
        update = ','.join([f'{column} = :{column}' for column in dict_update.keys()])

        where = ' AND '.join([f"{k} IN :{k}" if isinstance(v, list) else f"{k} = :{k}" for k, v in dict_filter.items()])
        query = f'UPDATE {table_name} SET {update} WHERE {where} RETURNING {pk_name};'
        dict_update.update(dict_filter)

        result = await self.__query(query=query, parameters=dict_update, is_commit=True)


        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)



    async def save(self, table_name: str, dict_save: Dict[str, Any], pk_name: str = 'id',
                  returning: Optional[str] = None, is_values_list: bool = True,
                  is_first: bool = True) -> Union[Dict[str, Any], List[Any], Any]:
        returning = returning or pk_name
        dict_save = self.__build_log(dict_save, log_type='save')
        columns = ','.join(dict_save.keys())
        values = ','.join([f':{k}' for k in dict_save])
        update = ','.join([f'{k} = :{k}' for k in dict_save])

        query = f"""
            INSERT INTO {table_name}({columns}) VALUES ({values})
            ON CONFLICT ({pk_name}) DO UPDATE SET {update}
            RETURNING {returning};
        """
        result = await self.__query(query=query, parameters=dict_save, is_commit=True)
        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)



    async def insert(self, table_name: str, dict_insert: Dict[str, Any], pk_name: str = 'id',
                    is_values_list: bool = True, is_first: bool = True,
                    returning: Optional[str] = None) -> Union[Dict[str, Any], List[Any], Any]:
        if not dict_insert:
            return None
        returning = returning or pk_name
        dict_insert = self.__build_log(dict_insert, log_type='insert')
        columns = ','.join(dict_insert.keys())
        values = ','.join([f":{k}" for k in dict_insert])

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING {returning}"
        result = await self.__query(query=query, parameters=dict_insert, is_commit=True)
        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)


    async def bulk_insert(self, table_name: str, list_dict_insert: List[Dict[str, Any]],
                         pk_name: str = 'id', is_values_list: bool = True,
                         is_first: bool = False, returning: Optional[str] = None) -> Union[Dict[str, Any], List[Any], Any]:
        if not list_dict_insert:
            return None
        returning = returning or pk_name

        columns = ''
        values = ''
        parameters = {}

        for count, dict_insert in enumerate(list_dict_insert):
            dict_insert = self.__build_log(dict_insert, 'insert')
            if not columns:
                columns = ','.join(dict_insert.keys())

            values_name = ','.join([f":{k}_{count}" for k in dict_insert])
            for k, v in dict_insert.items():
                parameters[f"{k}_{count}"] = v
            values += f"({values_name}),"
        values = values.rstrip(',')

        query = f'INSERT INTO {table_name}({columns}) VALUES {values} RETURNING {returning};'
        result = await self.__query(query=query, parameters=parameters, is_commit=True)
        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)


    async def disable(self, table_name: str, dict_filter: Dict[str, Any],
                     is_values_list: bool = True, is_first: bool = False,
                     pk_name: str = 'id') -> Union[Dict[str, Any], List[Any], Any]:
        dict_update = {'status': False}
        return await self.update(
            table_name=table_name,
            dict_update=dict_update,
            dict_filter=dict_filter,
            is_disable=True,
            is_values_list=is_values_list,
            is_first=is_first,
            pk_name=pk_name
        )
