from sqlalchemy import Boolean, Column, DateTime, Identity, Integer, Numeric, String, Text, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    uid = Column(Integer, nullable=False)
    iid = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    pid = Column(Integer, nullable=False)
    uid = Column(Integer, nullable=False)
    price = Column(Numeric(14, 2), nullable=False)
    quantity = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    uid = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    create_at = Column(DateTime, nullable=False)
    tel = Column(String(31), nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    uid = Column(Integer, nullable=False)
    name = Column(Text, nullable=False, unique=True)
    category = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    oid = Column(Integer, nullable=False)
    iid = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    fulfillment = Column(Boolean, nullable=False, server_default=text('false'))


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    uid = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    upid = Column(Integer, nullable=False)
    rate = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=text('now()'))


class ReviewLike(Base):
    __tablename__ = 'review_like'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    rid = Column(Integer, nullable=False)
    uid = Column(Integer, nullable=False)
    is_up = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    balance = Column(Numeric(12, 2), nullable=False)
