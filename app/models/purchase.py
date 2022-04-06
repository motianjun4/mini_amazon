from datetime import datetime
from typing import Union, List
from flask import current_app as app
from ..db import DB
from .orm.orm_models import Purchase as PurchaseORM, Order as OrderORM, Inventory as InventoryORM, Product as ProductORM
from sqlalchemy.orm.query import Query

class Purchase():
    def __init__(self, id, oid, iid, count, fulfillment, fulfill_at):
        self.id = id
        self.oid = oid
        self.iid = iid
        self.count = count
        self.fulfillment = fulfillment
        self.fulfillat = fulfill_at

    @staticmethod
    def get(id:int)->PurchaseORM:
        db:DB = app.db
        res:PurchaseORM = db.get_session().query(PurchaseORM).get(id)
        return res


    @staticmethod
    def get_all_by_uid(uid)->Union[Query, List[PurchaseORM]]:
        # return app.db.get_session().query(PurchaseORM).filter(PurchaseORM.order.has(uid=10))
        return app.db.get_session().query(PurchaseORM).join(OrderORM).filter(OrderORM.uid==uid)

    @staticmethod
    def get_money_spend_by_uid(uid)->str:
        sql = '''
        select sum(price*"count")
from purchase
join "order" ON purchase.oid = "order".id
where "order".uid = :uid
        '''
        rows = app.db.execute(sql, uid=uid)
        return rows[0][0] or "0.00"

    @staticmethod
    def get_items_bought_by_uid(uid) -> str:
        sql = '''
        select sum("count")
from purchase
join "order" ON purchase.oid = "order".id
where "order".uid = :uid
        '''
        rows = app.db.execute(sql, uid=uid)
        return rows[0][0] or "0"

    @staticmethod
    def fulfill(id:int, fulfill_at:datetime)->bool:
        app.db.execute('''
            UPDATE purchase
            SET fulfillment = TRUE, fulfill_at = :fulfill_at
            WHERE id = :id
        ''', id=id, fulfill_at=fulfill_at)
        return True

    @staticmethod
    def place_order(oid, purchase_list):
        sql = "INSERT INTO purchase(oid, iid, price, count, fulfillment) VALUES"
        for purchase in purchase_list:
            sql += " ("+str(oid)+","+str(purchase[0])+","+str(purchase[1])+","+str(purchase[2])+",false),"
        sql = sql[:-1]
        app.db.execute(sql)
