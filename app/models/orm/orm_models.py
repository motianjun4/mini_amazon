from sqlalchemy import Boolean, Column, DateTime, Identity, Integer, Numeric, String, Text, text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    uid = Column(Integer, ForeignKey('user.id') ,nullable=False)
    iid = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    pid = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship("Product", back_populates="inventories", lazy=False)
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
    purchases = relationship("Purchase", back_populates="order", lazy=False)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    uid = Column(Integer, nullable=False)
    name = Column(Text, nullable=False, unique=True)
    category = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    inventories = relationship("Inventory", back_populates="product", lazy='dynamic')


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    oid = Column(Integer,ForeignKey('order.id'), nullable=False)
    order = relationship("Order", back_populates="purchases", lazy=False)
    iid = Column(Integer,ForeignKey('inventory.id'), nullable=False)
    inventory = relationship("Inventory", lazy=False)
    count = Column(Integer, nullable=False)
    fulfillment = Column(Boolean, nullable=False, server_default=text('false'))


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    uid = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    target_uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    target_user = relationship("User")
    target_pid = Column(Integer, ForeignKey('product.id'), nullable=False)
    target_product = relationship("Product")
    rate = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=text('now()'))
    review_likes = relationship("ReviewLike", back_populates="review")


class ReviewLike(Base):
    __tablename__ = 'review_like'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1,
                maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    rid = Column(Integer, ForeignKey('review.id'),nullable=False)
    review = relationship("Review", back_populates="review_likes")
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    creator = relationship("User")
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
