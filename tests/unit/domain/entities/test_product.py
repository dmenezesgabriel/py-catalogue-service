import unittest
from uuid import UUID, uuid4

from src.domain.entities import Category, Product
from src.domain.exceptions import (
    InvalidDescription,
    InvalidImageUrl,
    InvalidName,
    InvalidSku,
)
from src.domain.value_objects import Inventory, Price


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.valid_name = "Valid Product"
        self.short_name = "No"
        self.empty_name = ""
        self.none_name = None
        self.valid_description = "This is a valid description."
        self.short_description = "No"
        self.empty_description = ""
        self.none_description = None
        self.valid_sku = "12345"
        self.short_sku = "12"
        self.empty_sku = ""
        self.none_sku = None
        self.valid_image_url = "http://example.com/image.jpg"
        self.invalid_image_url = "example.com/image.jpg"
        self.valid_id = uuid4()
        self.valid_version = 1
        self.valid_price = Price(value=100, discount_percent=0.0)
        self.valid_inventory = Inventory(quantity=10, reserved=0)
        self.valid_category = Category(name="Electronics")

    def test_product_creation_with_id_and_version(self):
        product = Product(
            name=self.valid_name,
            description=self.valid_description,
            sku=self.valid_sku,
            image_url=self.valid_image_url,
            price=self.valid_price,
            inventory=self.valid_inventory,
            category=self.valid_category,
            version=self.valid_version,
            id=self.valid_id,
        )
        self.assertEqual(product.id, self.valid_id)
        self.assertEqual(product.version, self.valid_version)
        self.assertEqual(product.name, self.valid_name)
        self.assertEqual(product.description, self.valid_description)
        self.assertEqual(product.sku, self.valid_sku)
        self.assertEqual(product.image_url, self.valid_image_url)
        self.assertEqual(product.price, self.valid_price)
        self.assertEqual(product.inventory, self.valid_inventory)
        self.assertEqual(product.category, self.valid_category)

    def test_product_creation_without_id_and_version(self):
        product = Product(
            name=self.valid_name,
            description=self.valid_description,
            sku=self.valid_sku,
            image_url=self.valid_image_url,
            price=self.valid_price,
            inventory=self.valid_inventory,
            category=self.valid_category,
        )
        self.assertIsInstance(product.id, UUID)
        self.assertIsNone(product.version)
        self.assertEqual(product.name, self.valid_name)
        self.assertEqual(product.description, self.valid_description)
        self.assertEqual(product.sku, self.valid_sku)
        self.assertEqual(product.image_url, self.valid_image_url)
        self.assertEqual(product.price, self.valid_price)
        self.assertEqual(product.inventory, self.valid_inventory)
        self.assertEqual(product.category, self.valid_category)

    def test_validate_sku_valid(self):
        self.assertEqual(Product.validate_sku(self.valid_sku), self.valid_sku)

    def test_validate_sku_too_short(self):
        with self.assertRaises(InvalidSku) as context:
            Product.validate_sku(self.short_sku)
        self.assertEqual(
            str(context.exception), "Sku can not have less than 3 characters."
        )

    def test_validate_sku_empty(self):
        with self.assertRaises(InvalidSku) as context:
            Product.validate_sku(self.empty_sku)
        self.assertEqual(str(context.exception), "Sku field is mandatory")

    def test_validate_sku_none(self):
        with self.assertRaises(InvalidSku) as context:
            Product.validate_sku(self.none_sku)
        self.assertEqual(str(context.exception), "Sku field is mandatory")

    def test_validate_name_valid(self):
        self.assertEqual(
            Product.validate_name(self.valid_name), self.valid_name
        )

    def test_validate_name_too_short(self):
        with self.assertRaises(InvalidName) as context:
            Product.validate_name(self.short_name)
        self.assertEqual(
            str(context.exception), "Name can not have less than 3 characters."
        )

    def test_validate_name_empty(self):
        with self.assertRaises(InvalidName) as context:
            Product.validate_name(self.empty_name)
        self.assertEqual(str(context.exception), "Name field is mandatory.")

    def test_validate_name_none(self):
        with self.assertRaises(InvalidName) as context:
            Product.validate_name(self.none_name)
        self.assertEqual(str(context.exception), "Name field is mandatory.")

    def test_validate_description_valid(self):
        self.assertEqual(
            Product.validate_description(self.valid_description),
            self.valid_description,
        )

    def test_validate_description_too_short(self):
        with self.assertRaises(InvalidDescription) as context:
            Product.validate_description(self.short_description)
        self.assertEqual(
            str(context.exception),
            "Description can not have less than 3 characters.",
        )

    def test_validate_description_empty(self):
        with self.assertRaises(InvalidDescription) as context:
            Product.validate_description(self.empty_description)
        self.assertEqual(
            str(context.exception), "Description field is mandatory."
        )

    def test_validate_description_none(self):
        with self.assertRaises(InvalidDescription) as context:
            Product.validate_description(self.none_description)
        self.assertEqual(
            str(context.exception), "Description field is mandatory."
        )

    def test_validate_image_url_valid(self):
        self.assertEqual(
            Product.validate_image_url(self.valid_image_url),
            self.valid_image_url,
        )

    def test_validate_image_url_invalid(self):
        with self.assertRaises(InvalidImageUrl) as context:
            Product.validate_image_url(self.invalid_image_url)
        self.assertEqual(str(context.exception), "Image Url is invalid.")

    def test_validate_image_url_none(self):
        self.assertIsNone(Product.validate_image_url(None))

    def test_to_dict(self):
        product = Product(
            name=self.valid_name,
            description=self.valid_description,
            sku=self.valid_sku,
            image_url=self.valid_image_url,
            price=self.valid_price,
            inventory=self.valid_inventory,
            category=self.valid_category,
            version=self.valid_version,
            id=self.valid_id,
        )
        expected_dict = {
            "id": str(self.valid_id),
            "version": self.valid_version,
            "sku": self.valid_sku,
            "name": self.valid_name,
            "description": self.valid_description,
            "image_url": self.valid_image_url,
            "price": self.valid_price.to_dict(),
            "inventory": self.valid_inventory.to_dict(),
            "category": self.valid_category.to_dict(),
        }
        self.assertEqual(product.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
