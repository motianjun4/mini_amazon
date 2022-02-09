from flask import current_app as app
'''

CREATE TABLE IF NOT EXISTS public.accounts
(
    id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    uid integer NOT NULL,
    balance decimal(14, 2) NOT NULL,
    CONSTRAINT accounts_pkey PRIMARY KEY (id),
    CONSTRAINT accounts_uid_key UNIQUE (uid)
);

'''

class Account:
    def __init__(self, id, uid, balance=0):
        self.id = id
        self.uid = uid
        self.balance = balance

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, balance
FROM Accounts
WHERE id = :id
''',
                              id=id)
        return Account(*(rows[0])) if rows else None

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, balance
FROM Accounts
WHERE uid = :uid
''',
                              uid=uid,
                              )
        if not rows:
            rows = app.db.execute('''
INSERT INTO Accounts(uid, balance)
VALUES(:uid, :balance)
RETURNING id
            ''', uid=uid, balance=0)
            id = rows[0][0]
            return Account.get(id)
        return Account(*(rows[0])) if rows else None

    @staticmethod
    def deposit_by_uid(uid, amount):
        rows = app.db.execute('''
UPDATE Accounts
SET balance = balance + :amount
WHERE uid = :uid
RETURNING balance
        ''', uid=uid, amount=amount)
        balance = rows[0][0]
        return balance

