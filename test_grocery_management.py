import copy
import tempfile
import unittest
from pathlib import Path

import grocery_management as gm


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.inv = copy.deepcopy(gm.DEFAULT_INVENTORY)

    def test_add_item(self):
        gm.add_item(self.inv, "  Butter ", 55, 40)
        self.assertEqual(self.inv["butter"], {"price": 55, "stock": 40})

    def test_add_duplicate_item_fails(self):
        with self.assertRaises(ValueError):
            gm.add_item(self.inv, "milk", 25, 10)

    def test_add_item_rejects_bad_values(self):
        with self.assertRaises(ValueError):
            gm.add_item(self.inv, "", 10, 10)
        with self.assertRaises(ValueError):
            gm.add_item(self.inv, "tea", 0, 10)
        with self.assertRaises(ValueError):
            gm.add_item(self.inv, "tea", 10, -1)

    def test_restock_adds_to_existing_stock(self):
        gm.restock_item(self.inv, "MILK", 50)
        self.assertEqual(self.inv["milk"]["stock"], 200)

    def test_restock_missing_item_fails(self):
        with self.assertRaises(ValueError):
            gm.restock_item(self.inv, "pizza", 5)

    def test_change_price(self):
        gm.change_price(self.inv, "bread", 35)
        self.assertEqual(self.inv["bread"]["price"], 35)

    def test_delete_item_works_for_any_position(self):
        # The old version only ever checked the first item in the list.
        gm.delete_item(self.inv, "bread")
        self.assertNotIn("bread", self.inv)

    def test_delete_missing_item_fails(self):
        with self.assertRaises(ValueError):
            gm.delete_item(self.inv, "pizza")

    def test_stock_report_levels(self):
        self.inv["milk"]["stock"] = 5
        self.inv["egg"]["stock"] = 40
        report = {name: message for name, _, message in gm.stock_report(self.inv)}
        self.assertTrue(report["milk"].startswith("LOW"))
        self.assertTrue(report["egg"].startswith("CHECK"))
        self.assertNotIn("bread", report)


class BillingTests(unittest.TestCase):
    def setUp(self):
        self.inv = copy.deepcopy(gm.DEFAULT_INVENTORY)

    def test_simple_bill_has_no_discount(self):
        bill = gm.calculate_bill(self.inv, {"milk": 2, "bread": 1})
        self.assertEqual(bill["subtotal"], 80)
        self.assertEqual(bill["total"], 80)

    def test_bulk_discount_at_1000(self):
        bill = gm.calculate_bill(self.inv, {"chips": 20})   # 20 x 50 = 1000
        self.assertEqual(bill["bulk_discount"], 100)
        self.assertEqual(bill["total"], 900)

    def test_coupon_discount(self):
        bill = gm.calculate_bill(self.inv, {"milk": 4}, coupon="save10")
        self.assertEqual(bill["total"], 90)

    def test_bulk_and_coupon_stack(self):
        bill = gm.calculate_bill(self.inv, {"chips": 20}, coupon="SAVE10")
        self.assertEqual(bill["total"], 810)

    def test_wrong_coupon_is_ignored(self):
        bill = gm.calculate_bill(self.inv, {"milk": 4}, coupon="FREE")
        self.assertEqual(bill["total"], 100)

    def test_checkout_reduces_stock(self):
        gm.checkout(self.inv, {"milk": 10})
        self.assertEqual(self.inv["milk"]["stock"], 140)

    def test_checkout_fails_without_changing_anything(self):
        with self.assertRaises(ValueError):
            gm.checkout(self.inv, {"milk": 10, "egg": 5000})
        self.assertEqual(self.inv["milk"]["stock"], 150)


class SaveLoadTests(unittest.TestCase):
    def test_round_trip(self):
        inv = copy.deepcopy(gm.DEFAULT_INVENTORY)
        inv["milk"]["stock"] = 99
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "inv.json"
            gm.save_inventory(inv, path)
            self.assertEqual(gm.load_inventory(path), inv)

    def test_missing_file_gives_defaults(self):
        with tempfile.TemporaryDirectory() as folder:
            loaded = gm.load_inventory(Path(folder) / "nothing.json")
        self.assertEqual(loaded, gm.DEFAULT_INVENTORY)

    def test_old_format_or_broken_file_gives_defaults(self):
        with tempfile.TemporaryDirectory() as folder:
            old_format = Path(folder) / "old.json"
            old_format.write_text('[{"item": "milk", "price": 25, "amount": 130}]')
            broken = Path(folder) / "broken.json"
            broken.write_text("{ not json")
            self.assertEqual(gm.load_inventory(old_format), gm.DEFAULT_INVENTORY)
            self.assertEqual(gm.load_inventory(broken), gm.DEFAULT_INVENTORY)


if __name__ == "__main__":
    unittest.main()
