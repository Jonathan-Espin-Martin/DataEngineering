import mysql.connector
from mysql.connector import Error

def execute_queries():
    try:
            connection = mysql.connector.connect(
            host='localhost',
            database='library_online',
            user='sa',
            password='@Ubuntu123'
        )

        cursor = connection.cursor(dictionary=True)

        # Query 1: All books and their authors
        all_books_authors_query = """
        SELECT
            b.title, b.gender,
            b.published_year,
            CONCAT(a.name,' ',a.lastname) AS author,
            a.nationality
        FROM books b
        LEFT JOIN authors a
            ON b.author_id = a.author_id;
        """
        cursor.execute(all_books_authors_query)
        all_books_authors_results = cursor.fetchall()
        print("All Books and Authors:")
        for row in all_books_authors_results:
            print(row)
        print()

        # Query 2: All orders by customer
        all_orders_by_customer_query = """
        SELECT
            o.order_datetime,
            o.total_amount,
            CONCAT(c.name,' ',c.lastname) AS customer
        FROM orders o
        LEFT JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE c.customer_id LIKE '%';
        """
        cursor.execute(all_orders_by_customer_query)
        all_orders_by_customer_results = cursor.fetchall()
        print("All Orders by Customer:")
        for row in all_orders_by_customer_results:
            print(row)
        print()

        # Query 3: Spend by customer
        spend_by_customer_query = """
        SELECT
            MAX(CONCAT(c.name,' ',c.lastname)) AS customer,
            SUM(od.amount*od.unit_price) AS spend,
            MAX(b.title) AS book_name
        FROM orders o
        LEFT JOIN orders_details od
            ON o.order_id = od.order_id
        LEFT JOIN customers c
            ON c.customer_id = o.customer_id
        LEFT JOIN books b
            ON b.book_id = od.book_id
        GROUP BY c.customer_id, o.order_id;
        """
        cursor.execute(spend_by_customer_query)
        spend_by_customer_results = cursor.fetchall()
        print("Spend by Customer:")
        for row in spend_by_customer_results:
            print(row)
        print()

        # Query 4: Books by order
        book_by_order_query = """
        SELECT
            o.order_id,
            o.order_datetime,
            b.title AS book_name
        FROM orders o
        LEFT JOIN orders_details od
            ON od.order_id = o.order_id
        LEFT JOIN books b
            ON b.book_id = od.book_id
        WHERE o.order_id LIKE '%';
        """
        cursor.execute(book_by_order_query)
        book_by_order_results = cursor.fetchall()
        print("Books by Order:")
        for row in book_by_order_results:
            print(row)
        print()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Call the function to execute queries and print results
execute_queries()
