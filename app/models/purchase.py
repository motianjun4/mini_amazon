from flask import current_app as app


class Purchase():
    def __init__(self, id, oid, iid, count, fulfillment):
        self.id = id
        self.oid = oid
        self.iid = iid
        self.count = count
        self.fulfillment = fulfillment

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, oid, iid, count, fulfillment
FROM purchase
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT P.id, P.oid, P.iid, P.count, P.fulfillment
FROM purchase P
INNER JOIN "order" O ON O.id = P.oid
WHERE O.uid = :uid
AND O.create_at >= :since
ORDER BY O.create_at DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
