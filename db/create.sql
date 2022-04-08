-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

DROP TABLE IF EXISTS "user", "product", "cart", "inventory", "order", "purchase", "review", "review_like", "transaction";

CREATE TABLE IF NOT EXISTS "user" (
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    balance DECIMAL(12,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS "product" (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL,
    name TEXT UNIQUE NOT NULL,
    category VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
);

CREATE INDEX idx_product_uid ON "product" (uid);

CREATE TABLE IF NOT EXISTS "cart" (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL,
    iid INT NOT NULL,
    quantity INT NOT NULL
);

CREATE INDEX idx_cart_uid ON "cart" (uid);
CREATE INDEX idx_cart_iid ON "cart" (iid);

CREATE TABLE IF NOT EXISTS "inventory"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    pid integer NOT NULL,
    uid integer NOT NULL,
    price decimal(14, 2) NOT NULL,
    quantity integer NOT NULL
);

CREATE INDEX idx_inventory_pid ON "inventory"(pid);
CREATE INDEX idx_inventory_uid ON "inventory"(uid);

CREATE TABLE IF NOT EXISTS "order"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid integer NOT NULL,
    address varchar(255) NOT NULL,
    create_at timestamp NOT NULL,
    tel varchar(31) NOT NULL
);

CREATE INDEX idx_order_uid ON "order"(uid);

CREATE TABLE IF NOT EXISTS "purchase"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    oid integer NOT NULL,
    iid integer NOT NULL,
    price decimal(14,2) NOT NULL,
    count integer NOT NULL,
    fulfillment boolean NOT NULL DEFAULT FALSE,
    fulfill_at timestamp
);

CREATE INDEX idx_purchase_oid ON "purchase" (oid);
CREATE INDEX idx_purchase_iid ON "purchase" (iid);

CREATE TABLE IF NOT EXISTS "review"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid integer NOT NULL,
    type integer NOT NULL, -- 1 or 2, 1: upid set to uid; 2: upid set to pid
    target_uid integer NOT NULL,
    target_pid integer NOT NULL,
    rate integer NOT NULL,
    review text NOT NULL,
    create_at timestamp NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_review_uid ON "review" (uid);
CREATE INDEX idx_review_target_uid ON "review"(target_uid);
CREATE INDEX idx_review_target_pid ON "review"(target_pid);

CREATE TABLE IF NOT EXISTS "review_like"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    rid integer NOT NULL,
    uid integer NOT NULL,
    is_up integer NOT NULL
);

CREATE INDEX idx_review_like_rid ON "review_like"(rid);
CREATE INDEX idx_review_like_uid ON "review_like"(uid);

CREATE TABLE IF NOT EXISTS "transaction"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid integer NOT NULL,
    amount decimal(14,2) NOT NULL,
    type integer NOT NULL, -- 1: debit(inc); 2: credit(dec)
    balance decimal(14,2) NOT NULL,
    create_at timestamp NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_transaction_uid ON "transaction" (uid);
CREATE INDEX idx_transaction_create_at ON "transaction" (create_at);
