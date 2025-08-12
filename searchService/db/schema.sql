CREATE SCHEMA IF NOT EXISTS search;
CREATE TABLE IF NOT EXISTS search.index (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10,2)
);
