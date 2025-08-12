CREATE SCHEMA IF NOT EXISTS shipping;
CREATE TABLE IF NOT EXISTS shipping.shipments (
    shipment_id UUID PRIMARY KEY,
    order_id UUID NOT NULL,
    address TEXT NOT NULL,
    status TEXT NOT NULL
);
