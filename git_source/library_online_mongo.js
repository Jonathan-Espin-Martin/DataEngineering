db = db.getSiblingDB('library_online');
db.dropDatabase();

// Crear la colección de autores e insertar datos
let authors = [
    { _id: ObjectId(), name: "George", lastname: "Orwell", nationality: "British" },
    { _id: ObjectId(), name: "J.K.", lastname: "Rowling", nationality: "British" },
    { _id: ObjectId(), name: "Ernest", lastname: "Hemingway", nationality: "American" },
    { _id: ObjectId(), name: "Jane", lastname: "Austen", nationality: "British" },
    { _id: ObjectId(), name: "Mark", lastname: "Twain", nationality: "American" }
];
db.authors.insertMany(authors);

// Crear la colección de libros e insertar datos
let books = [
    { _id: ObjectId(), title: "1984", gender: "Dystopian", published_year: 1949, author_id: authors[0]._id },
    { _id: ObjectId(), title: "Harry Potter", gender: "Fantasy", published_year: 1997, author_id: authors[1]._id },
    { _id: ObjectId(), title: "The Old Man and the Sea", gender: "Fiction", published_year: 1952, author_id: authors[2]._id },
    { _id: ObjectId(), title: "Pride and Prejudice", gender: "Romance", published_year: 1813, author_id: authors[3]._id },
    { _id: ObjectId(), title: "Adventures of Huckleberry Finn", gender: "Adventure", published_year: 1884, author_id: authors[4]._id }
];
db.books.insertMany(books);

// Crear la colección de clientes e insertar datos
let customers = [
    { _id: ObjectId(), name: "John", lastname: "Doe", email: "john.doe@example.com", address: "123 Elm Street", phone_number: "1234567890" },
    { _id: ObjectId(), name: "Jane", lastname: "Smith", email: "jane.smith@example.com", address: "456 Oak Street", phone_number: "0987654321" },
    { _id: ObjectId(), name: "Alice", lastname: "Johnson", email: "alice.johnson@example.com", address: "789 Pine Street", phone_number: "1230984567" },
    { _id: ObjectId(), name: "Bob", lastname: "Brown", email: "bob.brown@example.com", address: "321 Maple Street", phone_number: "7890123456" },
    { _id: ObjectId(), name: "Charlie", lastname: "Davis", email: "charlie.davis@example.com", address: "654 Birch Street", phone_number: "4567890123" }
];
db.customers.insertMany(customers);

// Crear la colección de órdenes e insertar datos, incluyendo los detalles de las órdenes
db.orders.insertMany([
    { _id: ObjectId(), order_datetime: new Date(), customer_id: customers[0]._id, total_amount: 150, order_details: [{ book_id: books[0]._id, amount: 2, unit_price: 50.00 }] },
    { _id: ObjectId(), order_datetime: new Date(), customer_id: customers[1]._id, total_amount: 200, order_details: [{ book_id: books[1]._id, amount: 1, unit_price: 100.00 }] },
    { _id: ObjectId(), order_datetime: new Date(), customer_id: customers[2]._id, total_amount: 150, order_details: [{ book_id: books[2]._id, amount: 3, unit_price: 75.00 }] },
    { _id: ObjectId(), order_datetime: new Date(), customer_id: customers[3]._id, total_amount: 250, order_details: [{ book_id: books[3]._id, amount: 2, unit_price: 125.00 }] },
    { _id: ObjectId(), order_datetime: new Date(), customer_id: customers[4]._id, total_amount: 300, order_details: [{ book_id: books[4]._id, amount: 1, unit_price: 150.00 }] }
]);

print("Authors:");
printjson(db.authors.find().toArray());

print("Books:");
printjson(db.books.find().toArray());

print("Customers:");
printjson(db.customers.find().toArray());

print("Orders:");
printjson(db.orders.find().toArray());
