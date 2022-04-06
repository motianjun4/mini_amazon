from ctypes import Union
from typing import List
from flask import current_app as app
from flask_login import current_user

from app.models.utils import paginate_raw

class Product:
    def __init__(self, id, uid, name, category, description, iMinPrice=0, minPriceIid=None):
        self.id = id
        self.uid = uid
        self.name = name
        self.category = category
        self.description = description
        self.iMinPrice:Union[None, int] = iMinPrice
        self.minPriceIid = minPriceIid

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
    def get_all_by_keyword(has_seller=True, like:str="") -> List["Product"]:
        sql = f'''
SELECT DISTINCT ON (product.id) product.id, product.uid, name, category, description, inventory.price, inventory.id
FROM product
LEFT OUTER JOIN inventory ON inventory.pid = product.id 
WHERE LOWER(name) LIKE LOWER(:like)
{"AND inventory.id is not NULL" if has_seller else ""}
ORDER BY product.id, inventory.price
''' 
        rows = app.db.execute(sql, like=like)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all(has_seller=True, page=0, page_size=20):
       # a = if available_only: 1 else: 2
       # minPriceIid --> Sales volume (only in this function)
        sql = f'''
SELECT product.id, product.uid, name, category, description, MIN(Inventory.price), SUM(purchase.count) AS pt_num
FROM product LEFT OUTER JOIN inventory ON inventory.pid = product.id JOIN Purchase ON Inventory.id=Purchase.iid
WHERE fulfillment = TRUE 
GROUP BY product.id
ORDER BY pt_num DESC 
'''
# {"AND inventory.id is not NULL" if has_seller else ""}
        rows = app.db.execute(paginate_raw(sql, page, page_size))
        return [Product(*row) for row in rows]

    @staticmethod
    def createProduct(form, uid):
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

