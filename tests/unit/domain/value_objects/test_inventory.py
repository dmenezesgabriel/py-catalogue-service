import unittest
from uuid import UUID, uuid4

from src.domain.exceptions import InvalidInventory
from src.domain.value_objects import Inventory


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.valid_quantity = 100
        self.negative_quantity = -10
        self.none_quantity = None
        self.valid_reserved = 20
        self.negative_reserved = -5
        self.reserved_greater_than_quantity = 120
        self.none_reserved = None
        self.valid_id = uuid4()

    def test_inventory_creation_with_id(self):
        inventory = Inventory(
            quantity=self.valid_quantity,
            reserved=self.valid_reserved,
            id=self.valid_id,
        )
        self.assertEqual(inventory.id, self.valid_id)
        self.assertEqual(inventory.quantity, self.valid_quantity)
        self.assertEqual(inventory.reserved, self.valid_reserved)
        self.assertEqual(
            inventory.in_stock, self.valid_quantity - self.valid_reserved
        )

    def test_inventory_creation_without_id(self):
        inventory = Inventory(
            quantity=self.valid_quantity, reserved=self.valid_reserved
        )
        self.assertIsInstance(inventory.id, UUID)
        self.assertEqual(inventory.quantity, self.valid_quantity)
        self.assertEqual(inventory.reserved, self.valid_reserved)
        self.assertEqual(
            inventory.in_stock, self.valid_quantity - self.valid_reserved
        )

    def test_validate_quantity_valid(self):
        self.assertEqual(
            Inventory._validate_quantity(self.valid_quantity),
            self.valid_quantity,
        )

    def test_validate_quantity_negative(self):
        with self.assertRaises(InvalidInventory) as context:
            Inventory._validate_quantity(self.negative_quantity)
        self.assertEqual(
            str(context.exception), "Quantity can not be negative."
        )

    def test_validate_quantity_none(self):
        with self.assertRaises(InvalidInventory) as context:
            Inventory._validate_quantity(self.none_quantity)
        self.assertEqual(
            str(context.exception), "Quantity field is mandatory."
        )

    def test_validate_reserved_valid(self):
        self.assertEqual(
            Inventory._validate_reserved(
                self.valid_reserved, self.valid_quantity
            ),
            self.valid_reserved,
        )

    def test_validate_reserved_negative(self):
        with self.assertRaises(InvalidInventory) as context:
            Inventory._validate_reserved(
                self.negative_reserved, self.valid_quantity
            )
        self.assertEqual(
            str(context.exception), "Reserved can not be negative."
        )

    def test_validate_reserved_greater_than_quantity(self):
        with self.assertRaises(InvalidInventory) as context:
            Inventory._validate_reserved(
                self.reserved_greater_than_quantity, self.valid_quantity
            )
        self.assertEqual(
            str(context.exception), "Reserved can not be higher than quantity."
        )

    def test_validate_reserved_none(self):
        with self.assertRaises(InvalidInventory) as context:
            Inventory._validate_reserved(
                self.none_reserved, self.valid_quantity
            )
        self.assertEqual(
            str(context.exception), "Reserved field is mandatory."
        )

    def test_to_dict(self):
        inventory = Inventory(
            quantity=self.valid_quantity,
            reserved=self.valid_reserved,
            id=self.valid_id,
        )
        expected_dict = {
            "id": str(self.valid_id),
            "quantity": self.valid_quantity,
            "reserved": self.valid_reserved,
            "in_stock": self.valid_quantity - self.valid_reserved,
        }
        self.assertEqual(inventory.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
