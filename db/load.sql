\COPY public.user FROM 'generated/User.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.user_id_seq',
                         (SELECT MAX(id)+1 FROM public.user),
                         false);

\COPY public.product FROM 'generated/Product.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.product_id_seq',
                         (SELECT MAX(id)+1 FROM public.product),
                         false);

\COPY public.cart FROM 'generated/Cart.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.cart_id_seq',
                         (SELECT MAX(id)+1 FROM public.cart),
                         false);

\COPY public.inventory FROM 'generated/Inventory.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.inventory_id_seq',
                         (SELECT MAX(id)+1 FROM public.inventory),
                         false);

\COPY public.Order FROM 'generated/Order.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.Order_id_seq',
                         (SELECT MAX(id)+1 FROM public.Order),
                         false);

\COPY public.purchase FROM 'generated/Purchase.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchase_id_seq',
                         (SELECT MAX(id)+1 FROM public.purchase),
                         false);

\COPY public.review FROM 'generated/Review.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.review_id_seq',
                         (SELECT MAX(id)+1 FROM public.review),
                         false);

\COPY public.review_like FROM 'generated/ReviewLike.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.review_like_id_seq',
                         (SELECT MAX(id)+1 FROM public.review_like),
                         false);

\COPY public.transaction FROM 'generated/Transaction.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.transaction_id_seq',
                         (SELECT MAX(id)+1 FROM public.transaction),
                         false);

-- set balance field in transaction according to amount field
UPDATE "transaction"
SET balance = calc_balance
FROM
(select id, 
SUM(
	CASE
		WHEN type = 1 THEN amount
		WHEN type = 2 THEN -amount
	END
) OVER (PARTITION BY uid ORDER BY create_at) AS calc_balance
from "transaction") AS calc
WHERE calc.id="transaction".id

-- set balance field in user according to balance field in transaction
UPDATE "user"
SET balance = latest_balance
FROM
(SELECT distinct on (uid) uid, balance as latest_balance
FROM "transaction"
ORDER BY uid asc, create_at desc) AS t
WHERE id = uid
