CREATE SCHEMA IF NOT EXISTS customer;
CREATE TABLE IF NOT EXISTS customer.customers (
    customer_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT
);
