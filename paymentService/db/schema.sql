CREATE SCHEMA IF NOT EXISTS payment;
CREATE TABLE IF NOT EXISTS payment.payments (
    payment_id UUID PRIMARY KEY,
    order_id UUID NOT NULL,
    amount NUMERIC(10,2) NOT NULL CHECK(amount>0),
    status TEXT NOT NULL
);
