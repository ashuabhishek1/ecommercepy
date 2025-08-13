# Service Documentation

## Overview
A new optional field `cupon` (string) was added to both the `CartLine` database table and the `CartIn` model in the Cart Service. This allows cart lines to optionally store a coupon code.

## API Changes
None

## Database Changes
- Added new nullable column `cupon` (String) to `cart.CartLine` table.

## Impacted Systems
- Cart Service
- cart.CartLine database table