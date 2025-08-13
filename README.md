# Service Documentation

## Overview
A new optional field `cupon` (string) was added to both the `CartLine` database table and the `CartIn` entity model in the Cart Service. This allows cart lines to optionally store a coupon code.

## API Changes
- Added `cupon` field to the `CartIn` model (used in API payloads).

## Database Changes
- Added nullable `cupon` column to the `cart.CartLine` table.

## Impacted Systems
- Cart Service
- cart.CartLine database table
- CartIn entity model
