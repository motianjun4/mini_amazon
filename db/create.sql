-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

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

CREATE TABLE IF NOT EXISTS "cart" (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL,
    iid INT NOT NULL,
    quantity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS "inventory"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    pid integer NOT NULL,
    uid integer NOT NULL,
    price decimal(14, 2) NOT NULL,
    quantity integer NOT NULL
);

CREATE TABLE IF NOT EXISTS "order"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid integer NOT NULL,
    address varchar(255) NOT NULL,
    create_at timestamp NOT NULL,
    tel varchar(31) NOT NULL
);

CREATE TABLE IF NOT EXISTS "purchase"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    oid integer NOT NULL,
    iid integer NOT NULL,
    count integer NOT NULL,
    fulfillment boolean NOT NULL DEFAULT FALSE
);

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

CREATE TABLE IF NOT EXISTS "review_like"
(
    id integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    rid integer NOT NULL,
    uid integer NOT NULL,
    is_up integer NOT NULL
);