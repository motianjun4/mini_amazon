from asyncio.windows_events import NULL
from pickle import FALSE, TRUE
from unicodedata import name
from flask import current_app as app
from .product import Product
'''

CREATE TABLE IF NOT EXISTS public.inventory
(
    id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    pid integer NOT NULL,  //product id
    uid integer NOT NULL,  //user id
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
    count integer NOT NULL,
    fulfillment boolean NOT NULL DEFAULT 0,
    CONSTRAINT inventory_pkey PRIMARY KEY (id)
);

'''

class Inventory:
    def __init__(self, id, pid, uid, price, quantity=0):
        self.id = id
        self.pid = pid
        self.uid = uid
        self.price = price
        self.quantity = quantity

    @staticmethod
    def get_all_by_uid(uid):     #show all
        rows = app.db.execute('''
                            SELECT Inventory.id, pid, uid, price, quantity
                            FROM Inventory JOIN Product ON Inventory.pid = Product.id
                            WHERE uid = :uid
                            ''', uid=uid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_product_pid(name):
        row = app.db.execute('''
                            SELECT *
                            FROM Product
                            WHERE name = :name
                            ''', name=name)
        if row:
            return Product(*row[0]).id
        else:
            print("cannot find product!")
            return 

    @staticmethod
    def add_new_product(uid, pid, price): #for inventory
        rows = app.db.execute('''
                            INSERT INTO Inventory(pid, uid, price, quantity)
                            VALUES(:pid, :uid, :price, :quantity)
                            RETURNING id
                            ''', pid=pid, uid=uid, price=price, quantity=1)
        return

    @staticmethod
    def modify_quantity(uid, pid, pnum):   
        # have_num = app.db.execute('''
        #                         SELECT quantity
        #                         FROM Inventory
        #                         WHERE uid = :uid AND name = :name
        #                         ''',uid=uid, name=pname)
        # have_num = Inventory(*have_num[0]).quantity
        
        # # if not have_num and pnum<0:
        # #     return
        # if have_num+pnum<0:
        #     app.db.execute('''
        #                 DELETE FROM Inventory
        #                 WHERE uid = :uid AND name = :name
        #                 RETURNING quantity
        #                 ''', uid=uid, name = pname)
        #     return 
        # else:
        if pnum<0:
            print("quantity is less than 0!")  #exception!
            return 
        app.db.execute('''
                    UPDATE Inventory
                    SET quantity = :pnum
                    WHERE uid = :uid AND pid = :pid
                    RETURNING quantity
                    ''', uid=uid, pid = pid, pnum=pnum)
        return

    @staticmethod
    def remove_product(uid, pid):
        app.db.execute('''
                    DELETE FROM Inventory
                    WHERE uid = :uid AND pid = :pid
                    RETURNING quantity
                    ''', uid=uid, pid = pid)
        return

    # @staticmethod
    # def get_low_price(pname):
    #     low_price = app.db.execute('''
    #                             SELECT price
    #                             FROM Product
    #                             WHERE name = :pname
    #                             ORDER BY ASC
    #                             ''', name=pname)
    #     return low_price[0][0]

    @staticmethod
    def products_run_down(uid):
        rows = app.db.execute('''
                            SELECT *
                            FROM Inventory
                            WHERE uid=uid
                            ''', uid=uid)
        run_down_list = []
        for row in rows:
            if Inventory(*row).quantity<5:
                run_down_list.append((Inventory(*row).pid, Inventory(*row).quantity))
        return run_down_list
                   
        