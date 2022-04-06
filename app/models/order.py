from distutils.command.build import build
from itertools import count
from unicodedata import category, name
from flask import current_app as app
from .purchase import Purchase
from .inventory import Inventory
from .orm.orm_models import Order as OrderORM
'''

CREATE TABLE IF NOT EXISTS public.inventory
(
    id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    pid integer NOT NULL,
    uid integer NOT NULL,
    price decimal(14, 2) NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT inventory_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.order
(
    id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    uid integer NOT NULL,
    address varchar(255) NOT NULL,
    create_at datetime NOT NULL,
    tel varchar(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.purchase
(
    id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    oid integer NOT NULL,
    iid integer NOT NULL,
    price decimal(14, 2) NOT NULL,
    count integer NOT NULL,
    fulfillment boolean NOT NULL DEFAULT 0,
    CONSTRAINT inventory_pkey PRIMARY KEY (id)
);

'''

class Order:
    def __init__(self, id, iid, pid, purchase_id, address, tel, create_at, fulfillment, buid, firstname, lastname, product_name, total_amount):
        self.id = id #
        # self.uid = uid #ID for seller
        self.iid = iid
        self.pid = pid
        self.purchase_id = purchase_id
        self.address = address #
        self.tel = tel 
        self.create_at = create_at #
        # self.count = count #count category
        self.fulfillment = fulfillment #
        self.buid = buid #ID for buyer
        self.firstname = firstname
        self.lastname = lastname
        self.product_name = product_name
        self.total_amount = total_amount #total num of items

    @staticmethod
    def get(oid)->'OrderORM':
        return app.db.get_session().query(OrderORM).filter(OrderORM.id == oid).first()

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
                            SELECT "order".id, iid, product.id, purchase.id, address, tel, create_at, fulfillment, "order".uid, firstname, lastname, Product.name, Purchase.count
                            FROM "order" JOIN Purchase ON "order".id = Purchase.oid JOIN Inventory ON Inventory.id = Purchase.iid JOIN "user" ON "user".id = "order".uid JOIN Product ON Product.id = Inventory.pid
                            WHERE Inventory.uid = :uid
                            ORDER BY create_at DESC
                            ''', uid=uid)
        return [Order(*row) for row in rows]

    @staticmethod
    def get_fulfilled_by_uid(uid):
        rows = app.db.execute('''
                            SELECT "order".id, iid, address, tel, create_at, COUNT(purchase.iid), fulfillment, "order".uid, firstname, lastname, SUM(Purchase.count)
                            FROM "order" JOIN Purchase ON "order".id = Purchase.oid JOIN Inventory ON Inventory.id = Purchase.iid JOIN "user" ON "user".id = "order".uid
                            WHERE Inventory.uid = :uid AND fulfillment = TRUE
                            GROUP BY "order".id
                            ORDER BY create_at DESC
                            ''', uid=uid)
        return [Order(*row) for row in rows]

    @staticmethod
    def get_unfulfilled_by_uid(uid):
        rows = app.db.execute('''
                            SELECT "order".id, iid, address, tel, create_at, COUNT(purchase.iid), fulfillment, "order".uid, firstname, lastname, SUM(Purchase.count)
                            FROM "order" JOIN Purchase ON "order".id = Purchase.oid JOIN Inventory ON Inventory.id = Purchase.iid JOIN "user" ON "user".id = "order".uid
                            WHERE Inventory.uid = :uid AND fulfillment = FALSE
                            GROUP BY "order".id
                            ORDER BY create_at DESC
                            ''', uid=uid)
        return [Order(*row) for row in rows]

#     @staticmethod
#     def get_summary(id, uid):
#         rows = app.db.execute('''
# SELECT id, uid, address, date, amount, status
# FROM Order
# WHERE uid = :uid AND id = :id
# ''',
#                              uid=uid, id=id)
#         # list_ = []
#         for row in rows:
#             address = Order(*row).address
#             date = Order(*row).date
#             amount = Order(*row).amount
#             status = Order(*row).status
#         return (address, date, amount, status)


    @staticmethod
    def fullfill_order(iid):
        app.db.execute('''
                        UPDATE Purchase
                        SET fulfillment = TRUE
                        WHERE iid = :iid
                        ''', iid=iid)
        return

    @staticmethod
    def entire_fulfilled(oid): #from the buyer’s perspective
        rows = app.db.execute('''
                            SELECT *
                            FROM Purchase JOIN Inventory ON Inventory.id=Purchase.iid
                            WHERE oid = :oid AND fulfillment = FALSE
                            ''', oid=oid)
        if not rows:
            return True
        else:
            return False


########################detail order page same as Product/Cart
# quantities and unit prices, total price, Final price

    @staticmethod
    def order_page(uid): #uid is from buyer’s uid
        rows =  app.db.execute('''
                            SELECT Purchase.count, Purchase.price, Inventory.pid
                            FROM "order" JOIN Purchase ON "order".id = Purchase.oid JOIN Inventory ON Inventory.id = Purchase.iid
                            WHERE "order".uid = :uid
                            ''', uid=uid)
        final = 0
        order_list = []
        for row in rows:
            quantity = row[0]
            price = row[1]
            pid = row[2]
            total_price = quantity*price
            final+=total_price
            order_list.append((quantity, price, pid, total_price))
        return order_list

    @staticmethod
    def bought_from_seller(uid, sid):
        rows =  app.db.execute('''
                            SELECT Inventory.uid
                            FROM "order" JOIN Purchase ON "order".id = Purchase.oid JOIN Inventory ON Inventory.id = Purchase.iid
                            WHERE "order".uid = :uid
                            ''', uid=uid)
        for row in rows:
            if sid == row[0]:
                return True
        return False

    @staticmethod
    def order_final_price(uid): #uid is from buyer’s uid
        rows =  app.db.execute('''
                            SELECT Purchase.count, Purchase.price
                            FROM "order" JOIN Purchase ON "order".id = Purchase.oid JOIN Inventory ON Inventory.id = Purchase.iid
                            WHERE "order".uid = :uid
                            ''', uid=uid)
        final = 0
        for row in rows:
            quantity = row[0]
            price = row[1]
            total_price = quantity*price
            final+=total_price
        return final

########################visualization/analytics

    @staticmethod
    def products_trends():
        rows = app.db.execute('''
                            SELECT pid, COUNT(*)
                            FROM Purchase JOIN Inventory ON Inventory.id=Purchase.iid
                            WHERE fulfillment = TRUE
                            GROUP BY Inventory.pid
                            ORDER BY DESC 
                            LIMIT 15
                            ''')
        trends_list = []
        for row in rows:
            trends_list.append((row[0], row[1])) #(name, num)
        return trends_list

# additional feature(s): Add analytics about buyers who have worked with this seller, e.g., ratings, number of messages, etc.

    @staticmethod
    def analy_buyer(uid): #this uid is for seller
        pass