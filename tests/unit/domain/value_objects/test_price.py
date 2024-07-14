import unittest
from uuid import UUID, uuid4

from src.domain.exceptions import InvalidPrice
from src.domain.value_objects import Price


class TestPrice(unittest.TestCase):
    def setUp(self):
        self.valid_value = 100.0
        self.negative_value = -10.0
        self.none_value = None
        self.valid_discount = 0.1
        self.negative_discount = -0.1
        self.high_discount = 1.1
        self.none_discount = None
        self.valid_id = uuid4()

    def test_price_creation_with_id(self):
        price = Price(
            value=self.valid_value,
            discount_percent=self.valid_discount,
            id=self.valid_id,
        )
        self.assertEqual(price.id, self.valid_id)
        self.assertEqual(price.value, self.valid_value)
        self.assertEqual(price.discount_percent, self.valid_discount)
        self.assertEqual(
            price.discounted_price,
            self.valid_value * (1 - self.valid_discount),
        )

    def test_price_creation_without_id(self):
        price = Price(
            value=self.valid_value, discount_percent=self.valid_discount
        )
        self.assertIsInstance(price.id, UUID)
        self.assertEqual(price.value, self.valid_value)
        self.assertEqual(price.discount_percent, self.valid_discount)
        self.assertEqual(
            price.discounted_price,
            self.valid_value * (1 - self.valid_discount),
        )

    def test_validate_price_valid(self):
        self.assertEqual(
            Price._validate_price(self.valid_value), self.valid_value
        )

    def test_validate_price_negative(self):
        with self.assertRaises(InvalidPrice) as context:
            Price._validate_price(self.negative_value)
        self.assertEqual(
            str(context.exception), "Price value can not be negative."
        )

    def test_validate_price_none(self):
        with self.assertRaises(InvalidPrice) as context:
            Price._validate_price(self.none_value)
        self.assertEqual(
            str(context.exception), "Price value is a mandatory field."
        )

    def test_validate_discount_valid(self):
        self.assertEqual(
            Price._validate_discount(self.valid_discount), self.valid_discount
        )

    def test_validate_discount_negative(self):
        with self.assertRaises(InvalidPrice) as context:
            Price._validate_discount(self.negative_discount)
        self.assertEqual(
            str(context.exception), "Discount value can not be negative."
        )

    def test_validate_discount_high(self):
        with self.assertRaises(InvalidPrice) as context:
            Price._validate_discount(self.high_discount)
        self.assertEqual(
            str(context.exception),
            "Discount value can not be higher than 100%.",
        )

    def test_validate_discount_none(self):
        with self.assertRaises(InvalidPrice) as context:
            Price._validate_discount(self.none_discount)
        self.assertEqual(
            str(context.exception), "Discount value is a mandatory field."
        )

    def test_to_dict(self):
        price = Price(
            value=self.valid_value,
            discount_percent=self.valid_discount,
            id=self.valid_id,
        )
        expected_dict = {
            "id": str(self.valid_id),
            "value": self.valid_value,
            "discount_percent": self.valid_discount,
            "discounted_price": self.valid_value * (1 - self.valid_discount),
        }
        self.assertEqual(price.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
