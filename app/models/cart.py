from flask import current_app as app
from flask_login import current_user


class Cart:
    def __init__(self, cid, uid, sid, pName, pQuantity, pPrice, pDescription):
        self.cid = cid
        self.uid = uid
        self.sid = sid
        self.pName = pName
        self.pQuantity = pQuantity
        self.pPrice = pPrice
        self.pDesciption = pDescription
        self.quantity = pQuantity

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT Carts.id, Carts.uid, Carts.sid, products.name, Carts.quantity, sell.price, products.description
FROM Products, Carts, Sell
WHERE Carts.uid = :id and Carts.sid = Sell.id and Sell.pid = Products.id
''', id=uid)
        return [Cart(*row) for row in rows] if rows is not None else None


    @staticmethod
    def get_count(uid):
        cnt = app.db.execute('''
SELECT COUNT(*)
FROM Products, Carts, Sell
WHERE Carts.uid = :id and Carts.sid = Sell.id and Sell.pid = Products.id
''', id=uid)
        return cnt[0][0]


    @staticmethod
    def addCart(sid, numOfItems):
        app.db.execute("""
INSERT INTO Carts(uid, sid, quantity)
VALUES(:uid, :sid, :quantity)
RETURNING id
""", uid=current_user.id, sid=sid, quantity=numOfItems)
        rows = app.db.execute('''
SELECT Carts.uid, Carts.sid, products.name, sell.quantity, sell.price, products.description
FROM Products, Carts, Sell
WHERE Carts.uid = :id and Carts.sid = Sell.id and Sell.pid = Products.id
''', id=current_user.id)
        return [Cart(*row) for row in rows] if rows is not None else None
