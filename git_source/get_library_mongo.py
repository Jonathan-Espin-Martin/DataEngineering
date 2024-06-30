from pymongo import MongoClient
from pprint import pprint

# Conexión a la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.library_online

def all_books_authors():
    pipeline = [
        {
            "$lookup": {
                "from": "authors",
                "localField": "author_id",
                "foreignField": "_id",
                "as": "author_details"
            }
        },
        {
            "$unwind": "$author_details"
        },
        {
            "$project": {
                "title": 1,
                "gender": 1,
                "published_year": 1,
                "author": {
                    "$concat": ["$author_details.name", " ", "$author_details.lastname"]
                },
                "nationality": "$author_details.nationality"
            }
        }
    ]
    result = list(db.books.aggregate(pipeline))
    return result

def all_orders_by_customer():
    pipeline = [
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "customer_details"
            }
        },
        {
            "$unwind": "$customer_details"
        },
        {
            "$project": {
                "order_datetime": 1,
                "total_amount": 1,
                "customer": {
                    "$concat": ["$customer_details.name", " ", "$customer_details.lastname"]
                }
            }
        }
    ]
    result = list(db.orders.aggregate(pipeline))
    return result

def spend_by_customer():
    pipeline = [
        {
            "$unwind": "$order_details"
        },
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "customer_details"
            }
        },
        {
            "$unwind": "$customer_details"
        },
        {
            "$lookup": {
                "from": "books",
                "localField": "order_details.book_id",
                "foreignField": "_id",
                "as": "book_details"
            }
        },
        {
            "$unwind": "$book_details"
        },
        {
            "$group": {
                "_id": {
                    "customer_id": "$customer_details._id",
                    "order_id": "$_id"
                },
                "customer": {
                    "$first": {
                        "$concat": ["$customer_details.name", " ", "$customer_details.lastname"]
                    }
                },
                "spend": {
                    "$sum": {
                        "$multiply": ["$order_details.amount", "$order_details.unit_price"]
                    }
                },
                "book_name": {"$first": "$book_details.title"}
            }
        },
        {
            "$group": {
                "_id": "$_id.customer_id",
                "customer": {"$first": "$customer"},
                "spend": {"$sum": "$spend"},
                "book_name": {"$first": "$book_name"}
            }
        }
    ]
    result = list(db.orders.aggregate(pipeline))
    return result

def book_by_order():
    pipeline = [
        {
            "$unwind": "$order_details"
        },
        {
            "$lookup": {
                "from": "books",
                "localField": "order_details.book_id",
                "foreignField": "_id",
                "as": "book_details"
            }
        },
        {
            "$unwind": "$book_details"
        },
        {
            "$project": {
                "order_id": 1,
                "order_datetime": 1,
                "book_name": "$book_details.title"
            }
        }
    ]
    result = list(db.orders.aggregate(pipeline))
    return result

print("All Books and Authors:")
pprint(all_books_authors())

print("\nAll Orders by Customer:")
pprint(all_orders_by_customer())

print("\nSpend by Customer:")
pprint(spend_by_customer())

print("\nBook by Order:")
pprint(book_by_order())
