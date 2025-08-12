CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE TABLE IF NOT EXISTS warehouse.stock (
    sku TEXT PRIMARY KEY,
    location TEXT NOT NULL DEFAULT 'MAIN',
    quantity INTEGER NOT NULL CHECK(quantity>=0),
    wcode TEXT NOT NULL
);
