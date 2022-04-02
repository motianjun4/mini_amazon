from flask import current_app as app
from flask_login import current_user


class Product:
    def __init__(self, id, uid, name, category, description):
        self.id = id
        self.uid = uid
        self.name = name
        self.category = category
        self.description = description

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
    def get_all(available_only=True, limit=100):
        sql = '''
SELECT product.id, product.uid, name, category, description
FROM product
'''

        if available_only: # if only show available items, select products that have inventory
            sql += '''
            INNER JOIN inventory ON inventory.uid = product.uid AND inventory.quantity > 0
            '''
        sql += "LIMIT :limit"
        rows = app.db.execute(sql, limit=limit)
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

