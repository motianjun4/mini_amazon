from datetime import datetime
from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_cart = 1000
num_inventories = 4000
num_orders = 100
num_reviews = 10000
num_review_likes = 10000

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def get_id(num):
    return fake.random_int(min=1, max=num)

def gen_users():
    with open('./generated/User.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('User...', end=' ', flush=True)
        for uid in range(1, num_users+1):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = f'{uid}@a.com'
            plain_password = f'password'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = fake.random_int(min=10, max=1000)
            writer.writerow([uid, email, password, firstname, lastname, balance])
        print(f'{num_users} generated')
    return


def gen_products():
    available_pids = []
    with open('./generated/Product.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product...', end=' ', flush=True)
        for pid in range(1, num_products+1):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            uid = get_id(num_users)
            name = fake.sentence(nb_words=10)[:-1]
            category = fake.random_element(elements=('Electronics', 'Sports', 'Food'))
            desc = fake.paragraph(nb_sentences=5)
            writer.writerow([pid, uid, name, category,
                            desc, ])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

def gen_cart():
    with open('./generated/Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for cid in range(1, num_cart+1):
            if cid % 100 == 0:
                print(f'{cid}', end=' ', flush=True)
            uid = get_id(num_users)
            iid = get_id(num_inventories)
            quantity = fake.random_int(min=1, max=10)
            writer.writerow([cid, uid, iid, quantity])
        print(f'{num_cart} generated')

def gen_inventory():
    with open('./generated/Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for iid in range(1, num_inventories+1):
            if iid % 100 == 0:
                print(f'{iid}', end=' ', flush=True)
            uid = get_id(num_users)
            pid = get_id(num_products)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            quantity = fake.random_int(min=0, max=1000)
            writer.writerow([iid, pid, uid, price, quantity])
        print(f'{num_inventories} generated')

def gen_order():
    with open('./generated/Order.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Order...', end=' ', flush=True)
        for oid in range(1, num_orders+1):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            uid = get_id(num_users)
            profile = fake.profile()
            address = profile['residence']
            past_datetime:datetime = fake.past_datetime()
            create_at = past_datetime.isoformat()
            tel = fake.phone_number()
            writer.writerow([oid, uid, address, create_at, tel])
        print(f'{num_orders} generated')


def gen_purchases():
    with open('./generated/Purchase.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchase...', end=' ', flush=True)
        for id in range(1, num_purchases+1):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            oid = get_id(num_orders)
            iid = get_id(num_inventories)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            count = fake.random_int(min=1, max=10)
            fulfillment = fake.random_int(min=0, max=1)
            if fulfillment:
                fulfill_at = fake.past_datetime().isoformat()
            writer.writerow(
                [id, oid, iid, price, count, fulfillment, fulfill_at])
        print(f'{num_purchases} generated')
    return


def gen_review():
    with open('./generated/Review.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Review...', end=' ', flush=True)
        for rid in range(1, num_reviews+1):
            if rid % 100 == 0:
                print(f'{rid}', end=' ', flush=True)
            uid = get_id(num_users)
            typ = fake.random_int(min=1, max=2)
            target_uid = 0
            target_pid = 0
            if typ == 1:
                target_uid = get_id(num_users)
            else:
                target_pid = get_id(num_products)
            oid = get_id(num_orders)
            iid = get_id(num_inventories)
            rate = fake.random_int(min=1, max=5)
            review = fake.paragraph(nb_sentences=2)
            past_datetime: datetime = fake.past_datetime()
            create_at = past_datetime.isoformat()
            writer.writerow([rid, uid, typ, target_uid, target_pid, rate, review, create_at])
        print(f'{num_reviews} generated')
    return


def gen_review_like():
    with open('./generated/ReviewLike.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ReviewLike...', end=' ', flush=True)
        for id in range(1, num_review_likes+1):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            rid = get_id(num_reviews)
            uid = get_id(num_users)
            is_up = fake.random_int(max=1)
            writer.writerow([id, rid, uid, is_up])
        print(f'{num_review_likes} generated')
    return


# gen_users()
# gen_products()
# gen_cart()
# gen_inventory()
# gen_order()
gen_purchases()
# gen_review()
# gen_review_like()