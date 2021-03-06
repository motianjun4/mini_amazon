
from flask import current_app as app
from typing import List

# from numpy import true_divide
from .product import Product
from .orm.orm_models import Inventory as InventoryORM
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
    price decimal(14, 2) NOT NULL,
    count integer NOT NULL,
    fulfillment boolean NOT NULL DEFAULT 0, 
    CONSTRAINT inventory_pkey PRIMARY KEY (id)
);

'''

class Inventory:
    def __init__(self, id, pid, uid, price, quantity, name):
        self.id = id
        self.pid = pid
        self.uid = uid
        self.price = price
        self.quantity = quantity
        self.name = name
        
    @staticmethod
    def get_all_by_uid(uid):     #show all
        rows = app.db.execute('''
                            SELECT Inventory.id, pid, Inventory.uid, Inventory.price, quantity, name
                            FROM Inventory JOIN Product ON Inventory.pid = Product.id
                            WHERE Inventory.uid = :uid
                            ''', uid=uid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_by_iid(uid, iid):     #show all
        rows = app.db.execute('''
                            SELECT Inventory.id, pid, Inventory.uid, Inventory.price, quantity, name
                            FROM Inventory JOIN Product ON Inventory.pid = Product.id
                            WHERE Inventory.uid = :uid AND Inventory.id = :iid
                            ''', uid=uid, iid=iid)
        return Inventory(*rows[0])

    @staticmethod
    def get_product_pid(form):
        row = app.db.execute('''
                            SELECT *
                            FROM Product
                            WHERE name = :name
                            ''', name=form.name.data)
        if row:
            return Product(*row[0]).id
        else:
            print("cannot find product!")
            return None
    
    @staticmethod
    def pid_in_inven(pid, uid):
        row = app.db.execute('''
                            SELECT *
                            FROM Inventory
                            WHERE pid = :pid and uid = :uid
                            ''', pid=pid, uid=uid)
        if row:
            return True
        else:
            return False

    @staticmethod
    def get_by_uid_ORM(uid) -> List[InventoryORM]:
        return app.db.get_session().query(InventoryORM).filter(InventoryORM.uid == uid)

    @staticmethod
    def add_new_product(form, uid, pid): #for inventory
        rows = app.db.execute('''
                            INSERT INTO Inventory(pid, uid, price, quantity)
                            VALUES(:pid, :uid, :price, :quantity)
                            RETURNING id
                            ''', pid=pid, uid=uid, price=form.price.data, quantity=form.quantity.data)
        return

    @staticmethod
    def modify_quantity(form, iid):   
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
        # if pnum<0:
        #     print("quantity is less than 0!")  #exception!
        #     return 
        app.db.execute('''
                    UPDATE Inventory
                    SET quantity = :pnum, price = :price
                    WHERE id = :iid
                    RETURNING quantity
                    ''', iid=iid, pnum=form.quantity.data, price=form.price.data)
        return

    @staticmethod
    def remove_product(iid):
        app.db.execute('''
                    DELETE FROM Inventory
                    WHERE id =:iid
                    RETURNING quantity
                    ''', iid=iid)
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
                            SELECT Inventory.id, pid, Inventory.uid, price, quantity, name
                            FROM Inventory JOIN Product ON Product.id = pid
                            WHERE Inventory.uid = :uid AND quantity<=6
                            ''', uid=uid)
        return [Inventory(*row) for row in rows]
                   
    @staticmethod
    def get_seller_list(pid):
        rows = app.db.execute('''
                            SELECT Inventory.price, Inventory.quantity, "user".firstname, "user".lastname, "user".id, inventory.id
                            FROM Inventory
                            LEFT JOIN "user" ON Inventory.uid="user".id
                            WHERE Inventory.pid=:pid
        ''', pid=pid)
        return rows

    @staticmethod
    def get_stock(iid_list):
        sql = "select id, quantity from inventory where id in ("
        for iid in iid_list:
            sql += str(iid) + ','
        sql=sql[:-1]+')'
        rows = app.db.execute(sql)
        return rows

    @staticmethod
    def reduce_inventory(iid_dict):
        sql = "UPDATE Inventory SET quantity = ( case"
        for k,v in iid_dict.items():
            sql += " when id=" + str(k) +" then quantity-" +str(v)
        sql += " end) where id in ("
        for k,_ in iid_dict.items():
            sql += str(k) + ','
        sql = sql[:-1]+')'
        app.db.execute(sql)

    @staticmethod
    def inventory_fulfill(uid):
        rows = app.db.execute('''
                            SELECT fulfillment, COUNT(*)
                            FROM Purchase JOIN Inventory ON Inventory.id=iid
                            WHERE uid = :uid
                            GROUP BY fulfillment
                            ''',uid=uid)
        fulfill = []
        for row in rows:
            if row[0]:
                fulfill.append((row[1],"fulfill"))
            else:
                fulfill.append((row[1],"unfulfill"))
        return fulfill

    @staticmethod
    def can_delete(uid, iid):
        rows = app.db.execute('''
                            SELECT iid
                            FROM Purchase JOIN Inventory ON Inventory.id=iid
                            WHERE uid = :uid AND iid = :iid
                            ''',uid=uid, iid=iid)
        if rows:
            return False
        else:
            return True