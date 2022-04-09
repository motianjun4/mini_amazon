from datetime import datetime
from typing import List
from flask import current_app as app
import pytz

from app.utils.time import get_now
from .orm.orm_models import Review as ReviewORM
import time
'''
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
'''
'''
rid 引用review.id, is_up 好评为1,差评为0
'''

class Review:
    def __init__(self):
        pass

    # get user review
    @staticmethod
    def get_all_by_tuid(tuid) -> List[ReviewORM]:
        return app.db.get_session().query(ReviewORM).filter(ReviewORM.target_uid == tuid)

    # get product review
    @staticmethod
    def get_all_by_tpid(tpid) -> List[ReviewORM]:
        return app.db.get_session().query(ReviewORM).filter(ReviewORM.target_pid == tpid)

    @staticmethod
    def submit(uid, type, target_uid, target_pid, rate, review):
        rows = app.db.execute('''
INSERT INTO review(uid, type, target_uid, target_pid, rate, review)
VALUES(:uid, :type, :target_uid, :target_pid, :rate, :review)
RETURNING id
        ''', uid=uid, type=type, target_uid=target_uid, target_pid=target_pid, rate=rate, review=review)
        return rows[0][0]

    @staticmethod
    def edit(uid, type, target_uid, target_pid, rate, review):
        rows = app.db.execute('''
UPDATE review
SET rate = :rate, review = :review, create_at=:create_at
WHERE uid = :uid
AND type = :type
AND target_uid = :target_uid
AND target_pid = :target_pid
RETURNING id
        ''', uid=uid, type=type, target_uid=target_uid, target_pid=target_pid, rate=rate, review=review, create_at=str(get_now()))
        return rows[0][0]

    @staticmethod
    def delete(uid, type, target_uid, target_pid):
        app.db.execute('''
DELETE FROM review
WHERE uid = :uid
AND type = :type
AND target_uid = :target_uid
AND target_pid = :target_pid
        ''', uid=uid, type=type, target_uid=target_uid, target_pid=target_pid)

    @staticmethod
    def show_review(uid, type, target_uid, target_pid):
        rows = app.db.execute('''
SELECT id, rate, review FROM review
WHERE uid = :uid
AND type = :type
AND target_uid = :target_uid
AND target_pid = :target_pid
        ''', uid=uid, type=type, target_uid=target_uid, target_pid=target_pid)
        return rows[0] if rows else None

    @staticmethod
    def show_review_list_user(uid, type):
        if type == 2:
            rows =app.db.execute('''
SELECT review.rate, review.review, product.name, product.id, review.create_at, review.id
FROM review
LEFT JOIN product ON product.id=review.target_pid
WHERE review.uid = :uid
AND type=2
ORDER BY create_at DESC
            ''', uid=uid)
            return rows
        elif type == 1:
            rows =app.db.execute('''
SELECT review.rate, review.review, "user".firstname, "user".lastname, "user".id, review.create_at, review.id
FROM review
LEFT JOIN "user" ON "user".id=review.target_uid
WHERE review.uid = :uid
AND type=1
ORDER BY create_at DESC
            ''', uid=uid)
            return rows

    @staticmethod
    def show_summary_review(type, target_uid, target_pid):
        rows = app.db.execute('''
SELECT AVG(rate) AS avg_rate, COUNT(*) AS review_cnt
FROM review
WHERE type=:type AND target_uid = :target_uid AND target_pid = :target_pid
        ''', type=type, target_uid=target_uid, target_pid=target_pid)
        return rows[0] if rows else None

class ReviewLike:
    def __init__(self, id, rid, uid, is_up):
        self.id = id
        self.rid = rid
        self.uid = uid
        self.is_up = is_up

    @staticmethod
    def insert(rid, uid, is_up):
        app.db.execute('''
INSERT INTO review_like(rid, uid, is_up)
VALUES(:rid, :uid, :is_up)
        ''', rid=rid, uid=uid, is_up=is_up)

    @staticmethod
    def delete(rid, uid):
        app.db.execute('''
DELETE FROM review_like
WHERE rid=:rid AND uid=:uid
        ''', rid=rid, uid=uid)

    @staticmethod
    def is_voted(rid, uid):
        rows = app.db.execute('''
SELECT id FROM review_like
WHERE rid=:rid AND uid=:uid
        ''', rid=rid, uid=uid)
        if len(rows) == 0:
            return False
        return True
