CREATE SCHEMA IF NOT EXISTS product;
CREATE TABLE IF NOT EXISTS product.products (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL CHECK(price>0),
    description TEXT
);
