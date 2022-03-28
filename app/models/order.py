from asyncio.windows_events import NULL
from unicodedata import name
from flask import current_app as app
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
    count integer NOT NULL,
    fulfillment boolean NOT NULL DEFAULT 0,
    CONSTRAINT inventory_pkey PRIMARY KEY (id)
);

'''

class Order:
    def __init__(self, id, uid, address, date, amount, status):
        self.id = id
        self.uid = uid
        self.address = address
        self.date = date
        self.amount = amount
        self.status = status

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, address, date, amount, status
FROM Order
WHERE uid = :uid
ORDER BY datetime DESC
''',
                             uid=uid)
        return [Order(*row) for row in rows]

    @staticmethod
    def get_fulfilled_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, address, date, amount, status
FROM Order
WHERE uid = :uid AND status = 1
ORDER BY datetime DESC
''',
                             uid=uid)
        return [Order(*row) for row in rows]

    @staticmethod
    def get_unfulfilled_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, address, date, amount, status
FROM Order
WHERE uid = :uid AND status = 0
ORDER BY datetime DESC
''',
                             uid=uid)
        return [Order(*row) for row in rows]

    @staticmethod
    def get_summary(id, uid):
        rows = app.db.execute('''
SELECT id, uid, address, date, amount, status
FROM Order
WHERE uid = :uid AND id = :id
''',
                             uid=uid, id=id)
        # list_ = []
        for row in rows:
            address = Order(*row).address
            date = Order(*row).date
            amount = Order(*row).amount
            status = Order(*row).status
        return (address, date, amount, status)

    @staticmethod
    def fullfill_order(uid, id):
        app.db.execute('''
                        UPDATE Order
                        SET status = 1
                        WHERE uid = :uid AND id = :id
                        ''', uid=uid, id=id)
        return


    
    



