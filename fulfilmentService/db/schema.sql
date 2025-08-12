CREATE SCHEMA IF NOT EXISTS fulfilment;
CREATE TABLE IF NOT EXISTS fulfilment.jobs (
    job_id UUID PRIMARY KEY,
    order_id UUID NOT NULL,
    status TEXT NOT NULL
);
