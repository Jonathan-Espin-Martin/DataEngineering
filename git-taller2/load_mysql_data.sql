CREATE DATABASE IF NOT EXISTS sales;
USE sales;

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    store_id INT,
    product_id INT,
    sales_amount FLOAT,
    transaction_date DATE
);

-- Insert data into the 'transactions' table
INSERT INTO transactions (store_id, product_id, sales_amount, transaction_date)
VALUES (3, 7, 137.45401188473625, '2020-01-01');
INSERT INTO transactions (store_id, product_id, sales_amount, transaction_date)
VALUES (4, 10, 195.07143064099163, '2020-01-02');
INSERT INTO transactions (store_id, product_id, sales_amount, transaction_date)
VALUES (1, 3, 173.1993941811405, '2020-01-03');
INSERT INTO transactions (store_id, product_id, sales_amount, transaction_date)
VALUES (3, 8, 159.86584841970367, '2020-01-04');
INSERT INTO transactions (store_id, product_id, sales_amount, transaction_date)
VALUES (3, 3, 115.60186404424365, '2020-01-05');