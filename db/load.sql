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