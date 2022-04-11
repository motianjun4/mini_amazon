from ctypes import Union
from typing import List
from flask import current_app as app
from flask_login import current_user
from .orm.orm_models import Product as ProductORM

class Product:
    def __init__(self, id, uid, name, category, description, iMinPrice=0, minPriceIid=None, avgRate=0, cnt=0):
        self.id = id
        self.uid = uid
        self.name = name
        self.category = category
        self.description = description
        self.iMinPrice:Union[None, int] = iMinPrice
        self.minPriceIid = minPriceIid
        self.avgRate=avgRate
        self.cnt=cnt

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, name, category, description
FROM product
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all_by_keyword(has_seller=True, like:str="", category:str="") -> List["Product"]:
        sql = f'''
SELECT DISTINCT ON (product.id) product.id, product.uid, name, category, description, inventory.price, inventory.id, AVG(rate) AS avgRate, SUM(purchase.count) AS cnt
FROM product
LEFT OUTER JOIN inventory ON inventory.pid = product.id 
LEFT JOIN review on product.id=review.target_pid
LEFT JOIN purchase on purchase.iid=inventory.id
WHERE LOWER(name) LIKE LOWER(:like)
{"AND inventory.id is not NULL" if has_seller else ""}
{"AND category = :category" if category else ""}
AND review.type=2
GROUP BY product.id, inventory.price, inventory.id
ORDER BY product.id DESC, inventory.price
''' 
        rows = app.db.execute(sql, like=like, category=category)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_ORM(uid)->List[ProductORM]:
        return app.db.get_session().query(ProductORM).filter(ProductORM.uid == uid).all()

    @staticmethod
    def get_all_by_name_ORM(name, pid)->List[ProductORM]:
        return app.db.get_session().query(ProductORM).filter(ProductORM.name == name).filter(ProductORM.id != pid).all()

    @staticmethod
    def get_all(has_seller=True):
       # a = if available_only: 1 else: 2
       # minPriceIid --> Sales volume (only in this function)
        sql = f'''
SELECT product.id, product.uid, name, category, description, MIN(Inventory.price), SUM(purchase.count) AS pt_num
FROM product LEFT OUTER JOIN inventory ON inventory.pid = product.id JOIN Purchase ON Inventory.id=Purchase.iid
WHERE fulfillment = TRUE 
GROUP BY product.id
ORDER BY product.id DESC, pt_num DESC 
LIMIT 20
'''
# {"AND inventory.id is not NULL" if has_seller else ""}
        rows = app.db.execute(sql)
        return [Product(*row) for row in rows]

    @staticmethod
    def product_create(form, uid):
        rows = app.db.execute("""
INSERT INTO product(name, category, description, uid)
VALUES(:name, :category, :description, :uid)
RETURNING id
""", name=form.product_name.data, category=form.category.data, description=form.description.data, uid=uid)
        pid = rows[0][0]

        rows = app.db.execute("""
INSERT INTO inventory(uid, pid, price, quantity)
VALUES(:uid, :pid, :price, :quantity)
RETURNING id
""", uid=current_user.id, pid=pid, price=form.price.data, quantity=form.quantity.data)
        iid = rows[0][0]
        return (pid, iid)

    @staticmethod
    def product_edit(form, pid):
        rows = app.db.execute("""
UPDATE product
SET name=:name, category=:category, description=:description
WHERE id = :pid
""", name=form.product_name.data, category=form.category.data, description=form.description.data, pid=pid)
        return rows

    @staticmethod
    def get_categories():
        rows = app.db.execute("""
SELECT DISTINCT category
FROM product
""")
        return [row[0] for row in rows]

    @staticmethod
    def get_total_sales(pid):
        rows = app.db.execute("""
SELECT SUM(purchase.count)
FROM purchase JOIN inventory ON purchase.iid = inventory.id
WHERE inventory.pid=:pid
""", pid=pid)
        return rows[0][0]
