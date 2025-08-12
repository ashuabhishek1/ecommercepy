CREATE SCHEMA IF NOT EXISTS orders;
CREATE TABLE IF NOT EXISTS orders.orders (
    order_id UUID PRIMARY KEY,
    cart_id TEXT NOT NULL,
    customer_id UUID NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS orders.order_lines (
    order_id UUID NOT NULL REFERENCES orders.orders(order_id) ON DELETE CASCADE,
    sku TEXT NOT NULL,
    qty INTEGER NOT NULL CHECK(qty>0),
    price NUMERIC(10,2) NOT NULL,
    PRIMARY KEY(order_id, sku)
);
