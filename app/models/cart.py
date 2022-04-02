from flask import current_app as app
from flask_login import current_user


class Cart:
    def __init__(self, cid, uid, iid, pName, pid, pQuantity, pPrice, pDescription):
        self.cid = cid
        self.uid = uid
        self.iid = iid
        self.pName = pName
        self.pid = pid
        self.pQuantity = pQuantity
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
