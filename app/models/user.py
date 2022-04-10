from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.transaction import Transaction

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, balance=0, sell_address=""):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.balance = balance
        self.sell_address = sell_address

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname
FROM "user"
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM "user"
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO "user"(email, password, firstname, lastname, balance)
VALUES(:email, :password, :firstname, :lastname, 0)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, balance, sell_address
FROM "user"
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def add_balance(id, amount):
        rows = app.db.execute('''
UPDATE "user"
SET balance = balance + :amount
WHERE id = :id
RETURNING balance
        ''', id=id, amount=amount)

        Transaction.insert(id, amount, rows[0][0])

        balance = rows[0][0]
        return balance

    @staticmethod
    def check_balance_enough(uid, price):
        rows = app.db.execute('''
select balance
from "user"
WHERE id = :id
        ''', id=uid)
        balance = rows[0][0]
        return True if balance >= price else False

    @staticmethod
    def update(id, email, firstname, lastname, sell_address):
        app.db.execute('''
UPDATE "user"
SET email = :email, firstname = :firstname, lastname = :lastname, sell_address = :sell_address
WHERE id = :id
        ''', id=id, email=email, firstname=firstname, lastname=lastname, sell_address=sell_address)
        return

    @staticmethod
    def update_password(id, password):
        app.db.execute('''
UPDATE "user"
SET password = :password
WHERE id = :id
        ''', id=id, password=generate_password_hash(password))
        return
