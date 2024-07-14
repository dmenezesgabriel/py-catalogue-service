import json
import unittest
from unittest.mock import Mock

from src.domain.entities import Product
from src.domain.enums import ProductEventType
from src.domain.events import ProductEvent


class TestProductEvent(unittest.TestCase):
    def setUp(self):
        self.mock_product = Mock(spec=Product)
        self.mock_product.to_dict.return_value = {
            "id": "1234",
            "version": 1,
            "sku": "testsku",
            "name": "Test Product",
            "description": "Test Description",
            "image_url": "http://example.com/image.jpg",
            "price": None,
            "inventory": None,
            "category": None,
        }
        self.valid_sku = "validsku"

    def test_product_event_creation_created_type_with_product(self):
        event = ProductEvent(
            type=ProductEventType.CREATED, product=self.mock_product
        )
        self.assertEqual(event.type, ProductEventType.CREATED)
        self.assertEqual(event.product, self.mock_product)
        self.assertIsNone(event.sku)

    def test_product_event_creation_updated_type_with_product(self):
        event = ProductEvent(
            type=ProductEventType.UPDATED, product=self.mock_product
        )
        self.assertEqual(event.type, ProductEventType.UPDATED)
        self.assertEqual(event.product, self.mock_product)
        self.assertIsNone(event.sku)

    def test_product_event_creation_deleted_type_with_sku(self):
        event = ProductEvent(type=ProductEventType.DELETED, sku=self.valid_sku)
        self.assertEqual(event.type, ProductEventType.DELETED)
        self.assertIsNone(event.product)
        self.assertEqual(event.sku, self.valid_sku)

    def test_product_event_creation_created_type_without_product(self):
        with self.assertRaises(Exception) as context:
            ProductEvent(type=ProductEventType.CREATED)
        self.assertEqual(
            str(context.exception),
            "CREATED product event must have valid product",
        )

    def test_product_event_creation_updated_type_without_product(self):
        with self.assertRaises(Exception) as context:
            ProductEvent(type=ProductEventType.UPDATED)
        self.assertEqual(
            str(context.exception),
            "UPDATED product event must have valid product",
        )

    def test_product_event_creation_deleted_type_without_sku(self):
        with self.assertRaises(Exception) as context:
            ProductEvent(type=ProductEventType.DELETED)
        self.assertEqual(
            str(context.exception), "DELETED product event must have valid sku"
        )

    def test_to_dict_with_product(self):
        event = ProductEvent(
            type=ProductEventType.CREATED, product=self.mock_product
        )
        expected_dict = {
            "type": ProductEventType.CREATED.string,
            "product": self.mock_product.to_dict(),
            "sku": None,
        }
        self.assertEqual(event.to_dict(), expected_dict)

    def test_to_dict_with_sku(self):
        event = ProductEvent(type=ProductEventType.DELETED, sku=self.valid_sku)
        expected_dict = {
            "type": ProductEventType.DELETED.string,
            "product": None,
            "sku": self.valid_sku,
        }
        self.assertEqual(event.to_dict(), expected_dict)

    def test_to_json_with_product(self):
        event = ProductEvent(
            type=ProductEventType.CREATED, product=self.mock_product
        )
        expected_json = json.dumps(
            {
                "type": ProductEventType.CREATED.string,
                "product": self.mock_product.to_dict(),
                "sku": None,
            }
        )
        self.assertEqual(event.to_json(), expected_json)

    def test_to_json_with_sku(self):
        event = ProductEvent(type=ProductEventType.DELETED, sku=self.valid_sku)
        expected_json = json.dumps(
            {
                "type": ProductEventType.DELETED.string,
                "product": None,
                "sku": self.valid_sku,
            }
        )
        self.assertEqual(event.to_json(), expected_json)


if __name__ == "__main__":
    unittest.main()
