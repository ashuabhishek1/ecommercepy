# E-Commerce Python Microservices with PostgreSQL

## Overview
This repository contains a complete **microservices-based e-commerce system** implemented in **Python (FastAPI)** with **PostgreSQL** databases for persistence, orchestrated using **Docker Compose**.

The system is broken down into **10 distinct services**, each with its own database schema and API, and a single PostgreSQL instance serving all schemas.  
Services communicate using **HTTP REST** and follow dependencies derived from the system’s architecture graph.

---

## Service List & Dependencies

Below is a list of all services, their purpose, and what they depend on.

### 1. **product_catalogueService**
- **Purpose:** Manages the master catalogue of products.
- **Endpoints:** Add product, Get product by SKU.
- **Dependencies:** None (root service).
- **Schema:** `product.products`

### 2. **cartService**
- **Purpose:** Manages shopping carts and their contents.
- **Endpoints:** Add item to cart, Get cart contents.
- **Dependencies:**
  - `product_catalogueService` – to validate SKUs exist before adding to cart.
- **Schema:** `cart.cartlines`

### 3. **orderService**
- **Purpose:** Creates orders from carts, calculates totals.
- **Endpoints:** Create order from cart, Get order by ID.
- **Dependencies:**
  - `cartService` – to fetch items in the cart.
  - `product_catalogueService` – to get current prices.
  - `customerService` – to verify customer exists.
- **Schema:** `orders.orders`, `orders.order_lines`

### 4. **transactionService**
- **Purpose:** Records payment transactions.
- **Endpoints:** Create transaction for order.
- **Dependencies:**
  - `orderService` – to confirm the order exists and total matches amount.
- **Schema:** `payment.transactions`

### 5. **customerService**
- **Purpose:** Maintains customer profiles.
- **Endpoints:** Create customer, Get customer by ID.
- **Dependencies:** None.
- **Schema:** `customer.customers`

### 6. **paymentService**
- **Purpose:** Processes payments for orders.
- **Endpoints:** Create payment for order.
- **Dependencies:**
  - `orderService` – to confirm the order exists and total matches.
- **Schema:** `payment.payments`

### 7. **searchService**
- **Purpose:** Stores searchable product index data.
- **Endpoints:** Index product data, Search products.
- **Dependencies:** None.
- **Schema:** `search.index`

### 8. **shippingService**
- **Purpose:** Creates shipping records for fulfilled orders.
- **Endpoints:** Create shipment.
- **Dependencies:**
  - `orderService` – to confirm order exists before shipping.
- **Schema:** `shipping.shipments`

### 9. **warehouseService**
- **Purpose:** Keeps track of inventory levels.
- **Endpoints:** Set stock, Get stock by SKU.
- **Dependencies:** None.
- **Schema:** `warehouse.stock`

### 10. **fulfilmentService**
- **Purpose:** Coordinates warehouse & shipping for an order.
- **Endpoints:** Fulfil order (reserve stock and create shipment).
- **Dependencies:**
  - `orderService` – to get order and its items.
  - `warehouseService` – to check sufficient stock is available.
  - `shippingService` – to create shipment for the order.
- **Schema:** `fulfilment.jobs`

---

## System Dependency Graph

graph TD product_catalogueService –> cartService product_catalogueService –> orderService cartService –> orderService customerService –> orderService orderService –> transactionService orderService –> paymentService orderService –> shippingService orderService –> fulfilmentService paymentService –> (none) transactionService –> (none) searchService –> (none) warehouseService –> fulfilmentService shippingService –> fulfilmentService

## Project Structure

ecommerce-python-pg-full/ ├── docker-compose.yml ├── product_catalogueService/ │   ├── app/main.py │   ├── db/schema.sql │   └── requirements.txt ├── cartService/ │   ├── app/main.py │   ├── db/schema.sql │   └── requirements.txt ├── orderService/ │   ├── app/main.py │   ├── db/schema.sql │   └── requirements.txt … (other services in same pattern)

## Running the Project

### Prerequisites
- **Docker** & **Docker Compose** installed
- Ports `8001`–`8010` and `5432` available




