from flask import current_app as app
from flask_login import current_user


class Product:
    def __init__(self, id, name, category, description, quantity, available, price):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.quantity = quantity
        self.available = available
        self.price = price

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, category, description, quantity, available
FROM Product
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT Sell.id, name, category, description, Product.quantity, available, price
FROM Product, Sell 
WHERE available = :available and Product.id = Sell.pid
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def createProduct(form):
        rows = app.db.execute("""
INSERT INTO Product(name, category, description, quantity, available)
VALUES(:name, :category, :description, :quantity, true)
RETURNING id
""", name=form.product_name.data, category=form.category.data, description=form.description.data, quantity=form.quantity.data)
        pid = rows[0][0]

        rows = app.db.execute("""
INSERT INTO Sell(uid, pid, price, quantity)
VALUES(:uid, :pid, :price, :quantity)
RETURNING id
""", uid=current_user.id, pid=pid, price=form.price.data, quantity=form.quantity.data)
        sid = rows[0][0]
        return sid

