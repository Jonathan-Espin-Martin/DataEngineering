db = db.getSiblingDB('library_online');
db.dropDatabase();

use library_online;

db.authors.insertMany([
    { name: "George", lastname: "Orwell", nationality: "British" },
    { name: "J.K.", lastname: "Rowling", nationality: "British" },
    { name: "Ernest", lastname: "Hemingway", nationality: "American" },
    { name: "Jane", lastname: "Austen", nationality: "British" },
    { name: "Mark", lastname: "Twain", nationality: "American" }
]);

db.books.insertMany([
    { title: "1984", gender: "Dystopian", published_year: 1949, author: { name: "George", lastname: "Orwell", nationality: "British" }},
    { title: "Harry Potter", gender: "Fantasy", published_year: 1997, author: { name: "J.K.", lastname: "Rowling", nationality: "British" }},
    { title: "The Old Man and the Sea", gender: "Fiction", published_year: 1952, author: { name: "Ernest", lastname: "Hemingway", nationality: "American" }},
    { title: "Pride and Prejudice", gender: "Romance", published_year: 1813, author: { name: "Jane", lastname: "Austen", nationality: "British" }},
    { title: "Adventures of Huckleberry Finn", gender: "Adventure", published_year: 1884, author: { name: "Mark", lastname: "Twain", nationality: "American" }}
]);

db.customers.insertMany([
    { name: "John", lastname: "Doe", email: "john.doe@example.com", address: "123 Elm Street", phone_number: "1234567890" },
    { name: "Jane", lastname: "Smith", email: "jane.smith@example.com", address: "456 Oak Street", phone_number: "0987654321" },
    { name: "Alice", lastname: "Johnson", email: "alice.johnson@example.com", address: "789 Pine Street", phone_number: "1230984567" },
    { name: "Bob", lastname: "Brown", email: "bob.brown@example.com", address: "321 Maple Street", phone_number: "7890123456" },
    { name: "Charlie", lastname: "Davis", email: "charlie.davis@example.com", address: "654 Birch Street", phone_number: "4567890123" }
]);

db.orders.insertMany([
    { order_datetime: new Date(), customer: { name: "John", lastname: "Doe" }, total_amount: 150, order_details: [{ book: { title: "1984", gender: "Dystopian", published_year: 1949, author: { name: "George", lastname: "Orwell", nationality: "British" }}, amount: 2, unit_price: 50.00 }]},
    { order_datetime: new Date(), customer: { name: "Jane", lastname: "Smith" }, total_amount: 200, order_details: [{ book: { title: "Harry Potter", gender: "Fantasy", published_year: 1997, author: { name: "J.K.", lastname: "Rowling", nationality: "British" }}, amount: 1, unit_price: 100.00 }]},
    { order_datetime: new Date(), customer: { name: "Alice", lastname: "Johnson" }, total_amount: 150, order_details: [{ book: { title: "The Old Man and the Sea", gender: "Fiction", published_year: 1952, author: { name: "Ernest", lastname: "Hemingway", nationality: "American" }}, amount: 3, unit_price: 75.00 }]},
    { order_datetime: new Date(), customer: { name: "Bob", lastname: "Brown" }, total_amount: 250, order_details: [{ book: { title: "Pride and Prejudice", gender: "Romance", published_year: 1813, author: { name: "Jane", lastname: "Austen", nationality: "British" }}, amount: 2, unit_price: 125.00 }]},
    { order_datetime: new Date(), customer: { name: "Charlie", lastname: "Davis" }, total_amount: 300, order_details: [{ book: { title: "Adventures of Huckleberry Finn", gender: "Adventure", published_year: 1884, author: { name: "Mark", lastname: "Twain", nationality: "American" }}, amount: 1, unit_price: 150.00 }]}
]);

print("Authors:");
printjson(db.authors.find().toArray());

print("Books:");
printjson(db.books.find().toArray());

print("Customers:");
printjson(db.customers.find().toArray());

print("Orders:");
printjson(db.orders.find().toArray());
