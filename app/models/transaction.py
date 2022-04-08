from flask import current_app as app

from app.utils.time import get_now

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
    def insert(uid, amount, balance):
        rows = app.db.execute('''
        insert into "transaction" (uid, amount, type, balance, create_at)
        values (:uid, :amount, :type, :balance, :create_at)
        returning id
        ''', uid=uid, amount=amount, type=1 if amount>0 else 2, balance=balance, create_at=get_now())
        return rows[0][0]

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
        SELECT id, uid, amount, type, balance, create_at
        FROM "transaction" 
        where uid = :uid
        order by create_at
        ''', uid=uid)
        return [Transaction(*row) for row in rows]
