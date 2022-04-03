from sqlalchemy.orm.query import Query

def paginate(query:Query, page:int=0, page_size:int=None)->Query:
    if page_size:
        query = query.limit(page_size)
    if page:
        query = query.offset(page*page_size)
    return query

def paginate_raw(sql:str, page:int=0, page_size:int=None)->str:
    if page_size:
        sql += f"\nLIMIT {page_size}"
    if page:
        sql += f"\nOFFSET {page*page_size}"
    return sql
