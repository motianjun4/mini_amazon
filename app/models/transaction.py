from flask import current_app as app

class Transaction():
    def __init__(self, id, uid, amount, type, balance, create_at):
        self.id = id
        self.uid = uid
        self.amount = amount
        self.type = type
        self.balance = balance
        self.create_at = create_at
        

    @staticmethod
    def get_balance_history_group_by_date(uid):
        rows = app.db.execute('''
        select distinct on (date(create_at)) date(create_at), balance
from "transaction"
where uid = 3
order by date(create_at) asc, create_at desc
        ''', uid=uid)
        return rows

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
        SELECT id, uid, amount, type, balance, create_at
        FROM "transaction" 
        where uid = :uid
        order by create_at
        ''', uid=uid)
        return [Transaction(*row) for row in rows]
