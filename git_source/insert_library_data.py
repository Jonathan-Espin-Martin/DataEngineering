import mysql.connector
from mysql.connector import Error

def insert_data():
    try:
        # Establish the connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='library_online',
            user='root',
            password='@Ubuntu123'
        )

        cursor = connection.cursor()

        # Insert data into the customers table
        customers_data = [
            ('John', 'Doe', 'john.doe@example.com', '123 Elm Street', '1234567890'),
            ('Jane', 'Smith', 'jane.smith@example.com', '456 Oak Street', '0987654321'),
            ('Alice', 'Johnson', 'alice.johnson@example.com', '789 Pine Street', '1230984567'),
            ('Bob', 'Brown', 'bob.brown@example.com', '321 Maple Street', '7890123456'),
            ('Charlie', 'Davis', 'charlie.davis@example.com', '654 Birch Street', '4567890123')
        ]
        cursor.executemany("""
            INSERT INTO customers (name, lastname, email, address, phone_number)
            VALUES (%s, %s, %s, %s, %s)
        """, customers_data)

        # Insert data into the authors table
        authors_data = [
            ('George', 'Orwell', 'British'),
            ('J.K.', 'Rowling', 'British'),
            ('Ernest', 'Hemingway', 'American'),
            ('Jane', 'Austen', 'British'),
            ('Mark', 'Twain', 'American')
        ]
        cursor.executemany("""
            INSERT INTO authors (name, lastname, nationality)
            VALUES (%s, %s, %s)
        """, authors_data)

        # Insert data into the books table
        books_data = [
            ('1984', 'Dystopian', 1949, 1),
            ('Harry Potter', 'Fantasy', 1997, 2),
            ('The Old Man and the Sea', 'Fiction', 1952, 3),
            ('Pride and Prejudice', 'Romance', 1813, 4),
            ('Adventures of Huckleberry Finn', 'Adventure', 1884, 5)
        ]
        cursor.executemany("""
            INSERT INTO books (title, gender, published_year, author_id)
            VALUES (%s, %s, %s, %s)
        """, books_data)

        # Insert data into the orders table
        orders_data = [
            (datetime.now(), 1, 100),
            (datetime.now(), 2, 200),
            (datetime.now(), 3, 150),
            (datetime.now(), 4, 250),
            (datetime.now(), 5, 300)
        ]
        cursor.executemany("""
            INSERT INTO orders (order_datetime, customer_id, total_amount)
            VALUES (%s, %s, %s)
        """, orders_data)

        # Insert data into the orders_details table
        orders_details_data = [
            (1, 1, 2, 50.00),
            (2, 2, 1, 100.00),
            (3, 3, 3, 75.00),
            (4, 4, 4, 125.00),
            (5, 5, 5, 150.00)
        ]
        cursor.executemany("""
            INSERT INTO orders_details (order_id, book_id, amount, unit_price)
            VALUES (%s, %s, %s, %s)
        """, orders_details_data)

        # Commit the transaction
        connection.commit()
        print("Records inserted successfully")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Call the function to insert data
insert_data()