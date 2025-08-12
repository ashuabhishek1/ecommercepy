CREATE SCHEMA IF NOT EXISTS cart;
CREATE TABLE IF NOT EXISTS cart.cartlines (
    cart_id TEXT NOT NULL,
    sku TEXT NOT NULL,
    qty INTEGER NOT NULL CHECK (qty>0),
    PRIMARY KEY (cart_id, sku)
);
