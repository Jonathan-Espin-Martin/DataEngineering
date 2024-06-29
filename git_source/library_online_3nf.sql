-- Create schema
CREATE DATABASE IF NOT EXISTS library_online;
USE library_online;

-- Create table 'customers'
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15) NOT NULL
);

-- Create table 'authors'
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    nationality VARCHAR(50) NOT NULL
);

-- Create table 'books'
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    gender VARCHAR(50) NOT NULL,
    published_year INT NOT NULL,
    author_id INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Create table 'orders'
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_datetime DATETIME NOT NULL,
    customer_id INT NOT NULL,
    total_amount INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create table 'orders_details'
CREATE TABLE orders_details (
    orders_details_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    book_id INT NOT NULL,
    amount INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);