db = db.getSiblingDB('library_online');
db.dropDatabase();

// Crear la colección de autores (sin insertar datos)
db.createCollection("authors");

// Crear la colección de libros (sin insertar datos)
db.createCollection("books");

// Crear la colección de clientes (sin insertar datos)
db.createCollection("customers");

// Crear la colección de órdenes (sin insertar datos)
db.createCollection("orders");

// Verificar que las colecciones fueron creadas
print("Collections in library_online database:");
printjson(db.getCollectionNames());
