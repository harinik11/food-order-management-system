# Online Food Order Management and Analysis System

A modular, menu-driven Python application designed for food ordering platforms to handle customer registrations, restaurant menus, dynamic cart creation, billing with discounts and delivery charges, order tracking, and sales analytics.

---

## Course Information
- **Course Code & Name:** CSA0801 - Python Programming
- **Topic:** Online Food Order Management and Analysis System
- **Level:** Bloom's Taxonomy L3 (Apply) & L4 (Analyse)

---

## Key Features
- **Customer Registration & Loyalty:** Stores customer profiles and loyalty program status in dictionaries.
- **Dynamic Restaurant Menus:** Multi-restaurant item catalog organized with lists and tuples.
- **Automated Billing Engine:** 
  - Tiered order discounts (up to 15%) + additional 5% loyalty discount.
  - Surcharge calculations for delivery based on order thresholds.
- **Order Lifecycle Tracking:** Real-time state transitions (`Placed` -> `Preparing` -> `Out for Delivery` -> `Delivered` / `Cancelled`).
- **Order Comparison:** Compares two distinct orders by item counts and net billed totals.
- **Performance & Analytics Report:** Computes total platform volume, unique ordering customers, cuisine distribution using sets, and per-restaurant sales revenue.
- **File Persistence:** Automatic flat-file storage (`food_orders.txt`) to maintain state between program executions.

---

## Python Data Structures Used
- **Dictionaries:** Fast $O(1)$ key-based access for customer accounts, menu indices, and structured order records.
- **Lists:** Ordered sequences of active restaurant orders and menu items.
- **Tuples:** Immutable records representing individual ordered items `(item_name, quantity, unit_price)`.
- **Sets:** Extraction and tracking of distinct menu categories and active customer IDs without duplicates.

---

## Project Structure
```text
Food-Order-Management-System/
├── food_delivery_system.py   # Main Python source code
├── food_orders.txt           # Persistent text storage for order records
└── README.md                 # Project documentation