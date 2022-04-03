from typing import Union, List
from flask import current_app as app
from ..db import DB
from .orm.orm_models import Purchase as PurchaseORM, Order as OrderORM, Inventory as InventoryORM, Product as ProductORM
from sqlalchemy.orm.query import Query

class Purchase():
    def __init__(self, id, oid, iid, count, fulfillment):
        self.id = id
        self.oid = oid
        self.iid = iid
        self.count = count
        self.fulfillment = fulfillment

    @staticmethod
    def get(id:int)->PurchaseORM:
        db:DB = app.db
        res:PurchaseORM = db.get_session().query(PurchaseORM).get(id)
        return res


    @staticmethod
    def get_all_by_uid(uid)->Union[Query, List[PurchaseORM]]:
        # return app.db.get_session().query(PurchaseORM).filter(PurchaseORM.order.has(uid=10))
        return app.db.get_session().query(PurchaseORM).join(OrderORM).filter(OrderORM.uid==uid)
