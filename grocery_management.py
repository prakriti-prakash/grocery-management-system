"""
Grocery Management System
-------------------------
A command-line program to manage a small grocery store: view and edit the
inventory, check stock levels, and bill customers.

Inventory is saved to inventory.json, so changes are kept between runs.
"""

import copy
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("inventory.json")

LOW_STOCK_LIMIT = 10          # at or below this: "LOW - restock now"
CHECK_STOCK_LIMIT = 50        # at or below this: "CHECK - running down"
BULK_DISCOUNT_THRESHOLD = 1000
BULK_DISCOUNT = 0.10          # 10% off bills of Rs. 1000 or more
COUPON_CODE = "SAVE10"
COUPON_DISCOUNT = 0.10        # extra 10% off with the coupon

DEFAULT_INVENTORY = {
    "milk":   {"price": 25, "stock": 150},
    "cereal": {"price": 10, "stock": 115},
    "chips":  {"price": 50, "stock": 120},
    "water":  {"price": 20, "stock": 185},
    "coffee": {"price": 45, "stock": 120},
    "egg":    {"price": 7,  "stock": 970},
    "bread":  {"price": 30, "stock": 230},
}


# ---------------------------------------------------------------------------
# Inventory logic (no input/output here, so it is easy to test)
# ---------------------------------------------------------------------------

def clean_name(name):
    """Make item names consistent: 'Milk ' and 'milk' are the same item."""
    return name.strip().lower()


def is_valid_inventory(data):
    """True if data looks like {"milk": {"price": 25, "stock": 150}, ...}."""
    return isinstance(data, dict) and all(
        isinstance(record, dict) and "price" in record and "stock" in record
        for record in data.values()
    )


def load_inventory(path=DATA_FILE):
    """Load the inventory from a JSON file, or start with the defaults."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return copy.deepcopy(DEFAULT_INVENTORY)
    if not is_valid_inventory(data):
        return copy.deepcopy(DEFAULT_INVENTORY)
    return data


def save_inventory(inventory, path=DATA_FILE):
    """Write the inventory to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=4)


def get_item(inventory, name):
    """Return the item's record, or raise ValueError if it does not exist."""
    name = clean_name(name)
    if name not in inventory:
        raise ValueError(f"'{name}' is not in the store.")
    return inventory[name]


def add_item(inventory, name, price, stock):
    name = clean_name(name)
    if not name:
        raise ValueError("Item name cannot be empty.")
    if name in inventory:
        raise ValueError(f"'{name}' already exists. Use restock instead.")
    if price <= 0:
        raise ValueError("Price must be greater than 0.")
    if stock < 0:
        raise ValueError("Stock cannot be negative.")
    inventory[name] = {"price": price, "stock": stock}


def restock_item(inventory, name, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    get_item(inventory, name)["stock"] += quantity


def change_price(inventory, name, new_price):
    if new_price <= 0:
        raise ValueError("Price must be greater than 0.")
    get_item(inventory, name)["price"] = new_price


def delete_item(inventory, name):
    get_item(inventory, name)          # raises ValueError if missing
    del inventory[clean_name(name)]


def stock_report(inventory):
    """Return (name, stock, message) for every item that is running low."""
    report = []
    for name, record in sorted(inventory.items()):
        stock = record["stock"]
        if stock <= LOW_STOCK_LIMIT:
            report.append((name, stock, "LOW - restock now"))
        elif stock <= CHECK_STOCK_LIMIT:
            report.append((name, stock, "CHECK - running down"))
    return report


# ---------------------------------------------------------------------------
# Billing logic
# ---------------------------------------------------------------------------

def calculate_bill(inventory, cart, coupon=""):
    """
    cart is a dict like {"milk": 2, "egg": 12}.
    Returns a dictionary with the bill lines, discounts and the final total.
    """
    lines = []
    subtotal = 0
    for name, quantity in cart.items():
        price = get_item(inventory, name)["price"]
        amount = price * quantity
        lines.append((name, quantity, price, amount))
        subtotal += amount

    total = subtotal
    bulk_discount = 0
    if total >= BULK_DISCOUNT_THRESHOLD:
        bulk_discount = total * BULK_DISCOUNT
        total -= bulk_discount

    coupon_discount = 0
    if coupon.strip().upper() == COUPON_CODE:
        coupon_discount = total * COUPON_DISCOUNT
        total -= coupon_discount

    return {
        "lines": lines,
        "subtotal": round(subtotal, 2),
        "bulk_discount": round(bulk_discount, 2),
        "coupon_discount": round(coupon_discount, 2),
        "total": round(total, 2),
    }


def checkout(inventory, cart):
    """Reduce stock for everything in the cart (checks stock first)."""
    for name, quantity in cart.items():
        available = get_item(inventory, name)["stock"]
        if quantity > available:
            raise ValueError(f"Only {available} units of '{name}' available.")
    for name, quantity in cart.items():
        inventory[name]["stock"] -= quantity


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def read_number(prompt, as_type=int):
    """Keep asking until the user types a valid number."""
    while True:
        try:
            return as_type(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def money(value):
    """Show 55.0 as 55 and 12.5 as 12.5, so prices look consistent."""
    return int(value) if value == int(value) else round(value, 2)


# ---------------------------------------------------------------------------
# Menu actions (these use input/print and call the logic above)
# ---------------------------------------------------------------------------

def show_store(inventory):
    if not inventory:
        print("The store is empty.")
        return
    print(f"\n{'Item':<15}{'Price (Rs.)':>12}{'In stock':>10}")
    print("-" * 37)
    for name, record in sorted(inventory.items()):
        print(f"{name:<15}{money(record['price']):>12}{record['stock']:>10}")
    print()


def add_item_menu(inventory):
    name = input("Enter item name: ")
    price = read_number("Enter the price of the item: ", float)
    stock = read_number("Enter the amount in stock: ")
    add_item(inventory, name, price, stock)
    print("Product added to the store.")


def restock_menu(inventory):
    name = input("Enter the name of the item to restock: ")
    quantity = read_number("Enter the quantity received: ")
    restock_item(inventory, name, quantity)
    print(f"Stock updated. Now in stock: {get_item(inventory, name)['stock']}")


def change_price_menu(inventory):
    name = input("Enter the name of the item: ")
    new_price = read_number("Enter the new price: ", float)
    change_price(inventory, name, new_price)
    print("Price updated.")


def delete_item_menu(inventory):
    name = input("Enter the name of the item to delete: ")
    delete_item(inventory, name)
    print("Item deleted.")


def check_item_menu(inventory):
    name = input("Enter the item you want to check: ")
    record = get_item(inventory, name)
    print(f"{clean_name(name)} - Rs. {money(record['price'])} - "
          f"{record['stock']} in stock")


def stock_report_menu(inventory):
    report = stock_report(inventory)
    if not report:
        print("All items are well stocked.")
        return
    for name, stock, message in report:
        print(f"{name:<15}{stock:>6} left   {message}")


def print_bill(bill):
    print(f"\n{'Item':<15}{'Qty':>5}{'Price':>9}{'Amount':>10}")
    print("-" * 39)
    for name, quantity, price, amount in bill["lines"]:
        print(f"{name:<15}{quantity:>5}{money(price):>9}{money(amount):>10}")
    print("-" * 39)
    print(f"{'Subtotal':<29}{money(bill['subtotal']):>10}")
    if bill["bulk_discount"]:
        print(f"{'Bulk discount (10%)':<29}{money(-bill['bulk_discount']):>10}")
    if bill["coupon_discount"]:
        print(f"{'Coupon discount (10%)':<29}{money(-bill['coupon_discount']):>10}")
    print(f"{'TOTAL (Rs.)':<29}{money(bill['total']):>10}\n")


def billing_menu(inventory):
    show_store(inventory)
    cart = {}
    while True:
        name = clean_name(input("Item to add to cart (or 'done' to finish): "))
        if name == "done":
            break
        if name not in inventory:
            print(f"'{name}' is not in the store.")
            continue
        quantity = read_number(f"Quantity of {name}: ")
        if quantity <= 0:
            print("Quantity must be greater than 0.")
            continue
        available = inventory[name]["stock"] - cart.get(name, 0)
        if quantity > available:
            print(f"Sorry, only {available} units available.")
            continue
        cart[name] = cart.get(name, 0) + quantity
        print(f"{quantity} units of {name} added to the cart.")

    if not cart:
        print("Cart is empty. Nothing to bill.")
        return

    coupon = input("Coupon code (press Enter to skip): ")
    bill = calculate_bill(inventory, cart, coupon)
    checkout(inventory, cart)
    print_bill(bill)


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

MENU = """
Grocery Store Management
1. View store
2. Add item to store
3. Restock an item
4. Change the price of an item
5. Billing
6. Delete item from store
7. Check one item
8. Low stock report
9. Exit
"""

ACTIONS = {
    1: show_store,
    2: add_item_menu,
    3: restock_menu,
    4: change_price_menu,
    5: billing_menu,
    6: delete_item_menu,
    7: check_item_menu,
    8: stock_report_menu,
}


def main():
    inventory = load_inventory()
    while True:
        print(MENU)
        choice = read_number("Enter your choice: ")
        if choice == 9:
            save_inventory(inventory)
            print("Inventory saved. Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice. Please pick a number from 1 to 9.")
            continue
        try:
            action(inventory)
        except ValueError as error:
            print(f"Error: {error}")
        save_inventory(inventory)


if __name__ == "__main__":
    main()
