# Grocery Management System

A command-line program, written in Python, for managing a small grocery store.
It started as a first-year project and has since been cleaned up, made more
reliable, and given tests.

## Features

- View all items with price and stock
- Add new items, restock existing ones, change prices, delete items
- Check the stock of a single item
- Low stock report (flags items at 10 or fewer, and 50 or fewer, units)
- Billing with an itemised receipt
  - 10% bulk discount on bills of Rs. 1000 or more
  - Extra 10% off with the coupon code `SAVE10`
- Inventory is saved to `inventory.json`, so changes are kept between runs
- Invalid input (letters instead of numbers, unknown items) shows a message
  instead of crashing the program

## Requirements

Python 3.8 or newer. No external libraries are needed.

## How to run

```
python grocery_management.py
```

## How to run the tests

```
python -m unittest -v
```

## Project structure

```
grocery-management-system/
├── grocery_management.py        # the program
├── test_grocery_management.py   # unit tests
├── v1/
│   └── grocery_management_v1.py # the original first-year version, kept for reference
├── README.md
└── .gitignore
```

`inventory.json` is created automatically on first run and is not tracked by git.

## What changed from the first version

| Problem in the original | Fix |
| --- | --- |
| Update and change-price printed "Item not found" for every non-matching item in the loop | Items are looked up directly by name, with one clear message |
| Delete only ever checked the first item in the list | Delete works for any item |
| Prompt said `done` but the code checked for `Done` | Input is case-insensitive |
| Stock was reduced as soon as an item went into the cart | Stock is reduced only at checkout, after everything is checked |
| Typing text where a number was expected crashed the program | Numbers are validated and the user is asked again |
| "Do you want to check the stock?" was asked twice, and the store was reprinted after every action | Store is shown only when asked for |
| `tracking_stock()` was written but never called | Now available as the low stock report |
| Data was lost when the program closed | Saved to `inventory.json` |
| Items stored as a list of dictionaries, searched by looping | Stored as a dictionary keyed by item name |
| Logic and `input()`/`print()` mixed together | Logic is separate, so it can be unit tested |

## Possible next steps

- Store the inventory in SQLite instead of JSON
- Add item categories and expiry dates
- Print or export bills to a file
- Build a simple GUI with Tkinter
