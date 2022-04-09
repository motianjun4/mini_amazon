from typing import List
from flask import current_app as app
from flask_login import current_user
from .orm.orm_models import Cart as CartORM


class Cart:
    def __init__(self, cid, uid, iid, pName, pid, pQuantity, pPrice, pDescription):
        self.cid = cid
        self.uid = uid
        self.iid = iid
        self.pName = pName
        self.pid = pid
        self.pPrice = pPrice
        self.pDesciption = pDescription
        self.quantity = pQuantity

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT cart.id, cart.uid, cart.iid, product.name, product.id, cart.quantity, inventory.price, product.description
FROM product, cart, inventory
WHERE cart.uid = :id and cart.iid = inventory.id and inventory.pid = product.id
''', id=uid)
        return [Cart(*row) for row in rows] if rows is not None else None

    @staticmethod
    def get_cart_by_uid_ORM(uid)->List[CartORM]:
        return app.db.get_session().query(CartORM).filter(CartORM.uid == uid).filter(CartORM.saved == False).all()

    @staticmethod
    def get_saved_by_uid_ORM(uid)->List[CartORM]:
        return app.db.get_session().query(CartORM).filter(CartORM.uid == uid).filter(CartORM.saved == True).all()

    @staticmethod
    def delete(cid):
        app.db.execute('''
DELETE FROM cart
WHERE id = :id
''', id=cid)

    @staticmethod
    def get_count(uid):
        cnt = app.db.execute('''
SELECT COUNT(*)
FROM product, cart, inventory
WHERE cart.uid = :id and cart.iid = inventory.id and inventory.pid = product.id
''', id=uid)
        return cnt[0][0]


    @staticmethod
    def addCart(iid, numOfItems):
        app.db.execute("""
INSERT INTO cart(uid, iid, quantity)
VALUES(:uid, :iid, :quantity)
RETURNING id
""", uid=current_user.id, iid=iid, quantity=numOfItems)

        rows = app.db.execute('''
SELECT cart.id, cart.uid, cart.iid, product.name, product.id, inventory.quantity, inventory.price, product.description
FROM product, cart, inventory
WHERE cart.uid = :id and cart.iid = inventory.id and inventory.pid = product.id
''', id=current_user.id)
        return [Cart(*row) for row in rows] if rows is not None else None

    @staticmethod
    def empty_cart(uid):
        app.db.execute("""
                    delete from cart
                    where uid=:uid
        """, uid=uid)

    @staticmethod
    def update_quantity(cid, quantity):
        app.db.execute("""
UPDATE cart
SET quantity = :quantity
WHERE id = :id
""", quantity=quantity, id=cid)

    @staticmethod
    def add_to_cart(cid):
        app.db.execute("""
UPDATE cart
SET saved = false
WHERE id = :id
""", id=cid)

    @staticmethod
    def save_cart_item(cid):
        app.db.execute("""
UPDATE cart
SET saved = true
WHERE id = :id
""", id=cid)
