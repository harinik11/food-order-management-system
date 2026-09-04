"""
Online Food Order Management and Analysis System
Course: CSA0801 - Python Programming
Demonstrates: Lists, Tuples, Dictionaries, Sets, File I/O, and String Formatting
"""

import os
import sys

DATA_FILE = "food_orders.txt"

# ---------------------------------------------------------
# GLOBAL IN-MEMORY STORAGE (Dictionaries, Lists, Sets)
# ---------------------------------------------------------
customers = {
    "C101": {"name": "Aravind Swamy", "phone": "9876543210", "is_member": True},
    "C102": {"name": "Meera Nambiar", "phone": "9845123456", "is_member": False},
}

# Restaurant Catalog: Dict of Lists containing Item Tuples (item_id, item_name, category, price)
restaurants = {
    "Aroma Biryani": [
        (1, "Chicken Dum Biryani", "Non-Veg", 240.0),
        (2, "Paneer Tikka Biryani", "Veg", 200.0),
        (3, "Mirchi Ka Salan", "Side", 50.0),
    ],
    "Green Leaf Cafe": [
        (1, "Garden Veggie Pizza", "Veg", 320.0),
        (2, "Mushroom Alfredo Pasta", "Veg", 280.0),
        (3, "Cold Coffee", "Beverage", 90.0),
    ],
    "Dragon Wok Express": [
        (1, "Schezwan Chicken Noodles", "Non-Veg", 220.0),
        (2, "Veg Spring Rolls", "Veg", 150.0),
        (3, "Manchow Soup", "Soup", 110.0),
    ]
}

# Master list of order dictionaries
orders = []
order_counter = 2000


# ---------------------------------------------------------
# UTILITY AND HELPER FUNCTIONS
# ---------------------------------------------------------
def generate_order_id():
    """Generates a sequential order ID."""
    global order_counter
    order_counter += 1
    return order_counter


def get_available_categories():
    """Extracts unique menu categories across all restaurants using a Set."""
    category_set = set()
    for item_list in restaurants.values():
        for item in item_list:
            category_set.add(item[2])
    return category_set


def calculate_billing(subtotal, is_member):
    """
    Computes discounts and delivery surcharges based on business rules.
    Returns: (discount_amount, delivery_fee, final_total)
    """
    # Tiered base discount
    if subtotal >= 800.0:
        discount_rate = 0.15
    elif subtotal >= 400.0:
        discount_rate = 0.10
    else:
        discount_rate = 0.0

    # Additional 5% for loyalty members
    if is_member:
        discount_rate += 0.05

    discount_amt = subtotal * discount_rate
    net_after_discount = subtotal - discount_amt

    # Tiered delivery charges
    if net_after_discount >= 500.0 or net_after_discount == 0.0:
        delivery_fee = 0.0
    elif net_after_discount >= 250.0:
        delivery_fee = 30.0
    else:
        delivery_fee = 50.0

    final_total = net_after_discount + delivery_fee
    return discount_amt, delivery_fee, final_total


# ---------------------------------------------------------
# CORE OPERATIONS
# ---------------------------------------------------------
def register_customer():
    """Registers a new customer profile into the dictionary."""
    print("\n--- Customer Registration ---")
    cust_id = input("Enter New Customer ID (e.g., C103): ").strip().upper()
    if cust_id in customers:
        print(f"Error: Customer ID {cust_id} is already registered.")
        return

    name = input("Enter Customer Name: ").strip().title()
    phone = input("Enter 10-Digit Contact Number: ").strip()

    if not (phone.isdigit() and len(phone) == 10):
        print("Validation Error: Invalid phone number format.")
        return

    member_choice = input("Enroll in Loyalty Program? (y/n): ").strip().lower()
    is_member = True if member_choice == 'y' else False

    customers[cust_id] = {"name": name, "phone": phone, "is_member": is_member}
    print(f"Customer '{name}' [ID: {cust_id}] registered successfully.")


def create_order():
    """Interactively creates, bills, and records an order."""
    print("\n--- Place New Food Order ---")
    cust_id = input("Enter Customer ID: ").strip().upper()
    if cust_id not in customers:
        print("Customer record not found. Please register first.")
        return

    print("\nAvailable Partner Restaurants:")
    rest_names = list(restaurants.keys())
    for idx, r_name in enumerate(rest_names, start=1):
        print(f"  {idx}. {r_name}")

    try:
        rest_choice = int(input("Select Restaurant Number: "))
        if rest_choice < 1 or rest_choice > len(rest_names):
            print("Invalid restaurant choice.")
            return
    except ValueError:
        print("Input error: Please enter a valid number.")
        return

    selected_restaurant = rest_names[rest_choice - 1]
    menu = restaurants[selected_restaurant]

    print(f"\n--- Menu: {selected_restaurant} ---")
    print(f"{'Code':<6} | {'Item Name':<26} | {'Category':<10} | {'Price (Rs)':<10}")
    print("-" * 60)
    for code, item_name, cat, price in menu:
        print(f"{code:<6} | {item_name:<26} | {cat:<10} | Rs {price:<8.2f}")

    ordered_items = []  # List of tuples: (item_name, qty, unit_price)
    subtotal = 0.0

    while True:
        try:
            item_code = int(input("\nEnter Item Code to add (0 to finish selection): "))
            if item_code == 0:
                break

            matched_item = None
            for item in menu:
                if item[0] == item_code:
                    matched_item = item
                    break

            if not matched_item:
                print("Invalid item code for this restaurant.")
                continue

            quantity = int(input(f"Enter quantity for '{matched_item[1]}': "))
            if quantity <= 0:
                print("Quantity must be at least 1.")
                continue

            line_cost = matched_item[3] * quantity
            subtotal += line_cost
            ordered_items.append((matched_item[1], quantity, matched_item[3]))
            print(f"Added: {quantity}x {matched_item[1]} (Rs {line_cost:.2f})")

        except ValueError:
            print("Please enter valid numeric values.")

    if not ordered_items:
        print("Order cancelled: No items selected.")
        return

    is_member = customers[cust_id]["is_member"]
    discount_amt, delivery_fee, final_total = calculate_billing(subtotal, is_member)
    new_order_id = generate_order_id()

    order_record = {
        "order_id": new_order_id,
        "cust_id": cust_id,
        "restaurant": selected_restaurant,
        "items": ordered_items,
        "subtotal": subtotal,
        "discount": discount_amt,
        "delivery_fee": delivery_fee,
        "final_total": final_total,
        "status": "Placed"
    }

    orders.append(order_record)

    # Print summary bill
    print("\n" + "=" * 45)
    print(f"ORDER SUMMARY CONFIRMATION [ID: #{new_order_id}]")
    print("=" * 45)
    print(f"Customer   : {customers[cust_id]['name']} ({cust_id})")
    print(f"Restaurant : {selected_restaurant}")
    print("-" * 45)
    for name, qty, price in ordered_items:
        print(f"{name:<25} x {qty:<2} = Rs {qty * price:>8.2f}")
    print("-" * 45)
    print(f"Subtotal            : Rs {subtotal:>8.2f}")
    print(f"Discount Applied    : -Rs {discount_amt:>7.2f}")
    print(f"Delivery Surcharge  : Rs {delivery_fee:>8.2f}")
    print(f"Final Payable Total : Rs {final_total:>8.2f}")
    print(f"Status              : Placed")
    print("=" * 45)


def update_order_status():
    """Updates the tracking status of an existing order."""
    print("\n--- Update Order Status ---")
    try:
        target_id = int(input("Enter Order ID to update: "))
    except ValueError:
        print("Invalid input format.")
        return

    for order in orders:
        if order["order_id"] == target_id:
            print(f"Current Status: {order['status']}")
            valid_statuses = ["Placed", "Preparing", "Out for Delivery", "Delivered", "Cancelled"]
            print(f"Allowed Statuses: {', '.join(valid_statuses)}")
            new_status = input("Enter new status: ").strip().title()

            if new_status in valid_statuses:
                order["status"] = new_status
                print(f"Order #{target_id} status updated to '{new_status}'.")
            else:
                print("Invalid status option. Update rejected.")
            return

    print(f"Order #{target_id} not found in active records.")


def compare_orders():
    """Custom Operation 1: Compares two orders by total amount."""
    print("\n--- Compare Two Orders ---")
    if len(orders) < 2:
        print("At least two orders must be registered to run a comparison.")
        return

    try:
        id1 = int(input("Enter First Order ID: "))
        id2 = int(input("Enter Second Order ID: "))
    except ValueError:
        print("Invalid input format.")
        return

    order1 = next((o for o in orders if o["order_id"] == id1), None)
    order2 = next((o for o in orders if o["order_id"] == id2), None)

    if not order1 or not order2:
        print("One or both Order IDs do not exist.")
        return

    print("\n" + "=" * 55)
    print(f"{'Attribute':<20} | {'Order #' + str(id1):<15} | {'Order #' + str(id2):<15}")
    print("-" * 55)
    print(f"{'Customer ID':<20} | {order1['cust_id']:<15} | {order2['cust_id']:<15}")
    print(f"{'Restaurant':<20} | {order1['restaurant'][:15]:<15} | {order2['restaurant'][:15]:<15}")
    print(f"{'Items Count':<20} | {sum(item[1] for item in order1['items']):<15} | {sum(item[1] for item in order2['items']):<15}")
    print(f"{'Net Billed Total':<20} | Rs {order1['final_total']:<12.2f} | Rs {order2['final_total']:<12.2f}")
    print("=" * 55)

    diff = abs(order1["final_total"] - order2["final_total"])
    if order1["final_total"] > order2["final_total"]:
        print(f"Verdict: Order #{id1} is larger by Rs {diff:.2f}")
    elif order2["final_total"] > order1["final_total"]:
        print(f"Verdict: Order #{id2} is larger by Rs {diff:.2f}")
    else:
        print("Verdict: Both orders have identical total values.")


def display_performance_report():
    """Custom Operation 2: Formatted order and restaurant analytics report."""
    print("\n" + "=" * 70)
    print("           PLATFORM PERFORMANCE & ANALYTICS REPORT")
    print("=" * 70)

    if not orders:
        print("No order transactions available to compile analytics.")
        return

    total_revenue = sum(o["final_total"] for o in orders if o["status"] != "Cancelled")
    unique_ordering_customers = {o["cust_id"] for o in orders}
    categories = get_available_categories()

    print(f"Total Transactions Logged : {len(orders)}")
    print(f"Net Realized Revenue      : Rs {total_revenue:.2f}")
    print(f"Active Unique Customers   : {len(unique_ordering_customers)}")
    print(f"Total Unique Cuisines/Cats: {len(categories)} ({', '.join(sorted(categories))})")

    # Status distribution
    status_counts = {}
    for o in orders:
        status_counts[o["status"]] = status_counts.get(o["status"], 0) + 1

    print("\nOrder Status Breakdown:")
    for status, count in status_counts.items():
        print(f"  - {status:<18}: {count}")

    # Restaurant sales breakdown
    print("\n" + "-" * 70)
    print(f"{'Restaurant Name':<28} | {'Orders':<8} | {'Total Volume (Rs)':<16}")
    print("-" * 70)

    for rest in restaurants:
        rest_orders = [o for o in orders if o["restaurant"] == rest and o["status"] != "Cancelled"]
        rest_revenue = sum(o["final_total"] for o in rest_orders)
        print(f"{rest:<28} | {len(rest_orders):<8} | Rs {rest_revenue:>12.2f}")
    print("=" * 70)


def save_orders_to_file():
    """Saves all active order records to a flat file."""
    try:
        with open(DATA_FILE, "w") as fp:
            for o in orders:
                items_str = ";".join([f"{name}*{qty}*{price}" for name, qty, price in o["items"]])
                line = (f"{o['order_id']}|{o['cust_id']}|{o['restaurant']}|"
                        f"{o['subtotal']:.2f}|{o['discount']:.2f}|{o['delivery_fee']:.2f}|"
                        f"{o['final_total']:.2f}|{o['status']}|{items_str}\n")
                fp.write(line)
        print(f"Successfully committed {len(orders)} order records to '{DATA_FILE}'.")
    except IOError as e:
        print(f"File Storage Error: {e}")


def load_orders_from_file():
    """Loads and restores order records from disk upon startup."""
    global order_counter
    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, "r") as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) == 9:
                    oid = int(parts[0])
                    cid = parts[1]
                    rest = parts[2]
                    subtotal = float(parts[3])
                    discount = float(parts[4])
                    delivery_fee = float(parts[5])
                    final_total = float(parts[6])
                    status = parts[7]

                    # Parse items list of tuples
                    items = []
                    item_tokens = parts[8].split(";")
                    for token in item_tokens:
                        if token:
                            t_name, t_qty, t_price = token.split("*")
                            items.append((t_name, int(t_qty), float(t_price)))

                    orders.append({
                        "order_id": oid,
                        "cust_id": cid,
                        "restaurant": rest,
                        "items": items,
                        "subtotal": subtotal,
                        "discount": discount,
                        "delivery_fee": delivery_fee,
                        "final_total": final_total,
                        "status": status
                    })
                    if oid > order_counter:
                        order_counter = oid
        print(f"Restored {len(orders)} order records from disk cache.")
    except (IOError, ValueError) as e:
        print(f"Warning: Error parsing persistent storage file ({e}).")


# ---------------------------------------------------------
# MAIN MENU CONTROLLER
# ---------------------------------------------------------
def main():
    load_orders_from_file()

    while True:
        print("\n==============================================")
        print("  ONLINE FOOD ORDER PLATFORM MANAGEMENT")
        print("==============================================")
        print("1. Register New Customer")
        print("2. Display Available Restaurant Menus")
        print("3. Place / Create New Order")
        print("4. Update Order Tracking Status")
        print("5. Compare Two Orders (Amount & Volume)")
        print("6. Generate Performance & Analytics Report")
        print("7. Save State & Exit")
        print("----------------------------------------------")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            register_customer()
        elif choice == '2':
            print("\n--- Available Food Catalogs ---")
            for rest_name, items in restaurants.items():
                print(f"\n[{rest_name}]")
                for code, name, cat, price in items:
                    print(f"  ({code}) {name:<24} [{cat:<8}] Rs {price:.2f}")
        elif choice == '3':
            create_order()
        elif choice == '4':
            update_order_status()
        elif choice == '5':
            compare_orders()
        elif choice == '6':
            display_performance_report()
        elif choice == '7':
            save_orders_to_file()
            print("System shutting down. All states synced.")
            break
        else:
            print("Invalid selection. Please choose an option between 1 and 7.")


if __name__ == "__main__":
    main()