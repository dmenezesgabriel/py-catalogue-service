import unittest
from unittest.mock import Mock

from src.domain.entities import Category, Product
from src.domain.exceptions import InvalidSku, ProductNotFound
from src.domain.services import CatalogueService
from src.domain.value_objects import Inventory, Price
from src.port import ProductEventPublisher, ProductRepository


class TestCatalogueService(unittest.TestCase):
    def setUp(self):
        self.mock_product_repository = Mock(spec=ProductRepository)
        self.mock_product_event_publisher = Mock(spec=ProductEventPublisher)
        self.catalogue_service = CatalogueService(
            product_repository=self.mock_product_repository,
            product_event_publisher=self.mock_product_event_publisher,
        )

    def test_create_product_success(self):
        mock_product = Mock(spec=Product)
        self.mock_product_repository.create_product.return_value = mock_product
        price = Mock(spec=Price)
        inventory = Mock(spec=Inventory)
        category = Mock(spec=Category)

        product = self.catalogue_service.create_product(
            sku="validsku",
            name="Valid Name",
            description="Valid Description",
            price=price,
            inventory=inventory,
            category=category,
            image_url="http://example.com/image.jpg",
        )

        self.assertEqual(product, mock_product)
        self.mock_product_event_publisher.publish.assert_called_once()

    def test_create_product_invalid_sku(self):
        with self.assertRaises(InvalidSku):
            self.catalogue_service.create_product(
                sku="", name="Valid Name", description="Valid Description"
            )

    def test_get_product_by_sku_success(self):
        mock_product = Mock(spec=Product)
        self.mock_product_repository.get_product_by_sku.return_value = (
            mock_product
        )

        product = self.catalogue_service.get_product_by_sku(sku="validsku")

        self.assertEqual(product, mock_product)

    def test_get_product_by_sku_not_found(self):
        self.mock_product_repository.get_product_by_sku.side_effect = (
            ProductNotFound("Product not found")
        )

        with self.assertRaises(ProductNotFound):
            self.catalogue_service.get_product_by_sku(sku="invalidsku")

    def test_update_product_success(self):
        mock_product = Mock(spec=Product)
        self.mock_product_repository.update_product.return_value = mock_product
        price = Mock(spec=Price)
        inventory = Mock(spec=Inventory)
        category = Mock(spec=Category)

        product = self.catalogue_service.update_product(
            sku="validsku",
            name="Updated Name",
            description="Updated Description",
            price=price,
            inventory=inventory,
            category=category,
            image_url="http://example.com/image.jpg",
        )

        self.assertEqual(product, mock_product)
        self.mock_product_event_publisher.publish.assert_called_once()

    def test_update_product_not_found(self):
        self.mock_product_repository.update_product.side_effect = (
            ProductNotFound("Product not found")
        )

        with self.assertRaises(ProductNotFound):
            self.catalogue_service.update_product(
                sku="invalidsku",
                name="Updated Name",
                description="Updated Description",
            )

    def test_delete_product_success(self):
        result = self.catalogue_service.delete_product(sku="validsku")

        self.assertTrue(result)
        self.mock_product_event_publisher.publish.assert_called_once()

    def test_delete_product_not_found(self):
        self.mock_product_repository.delete_product.side_effect = (
            ProductNotFound("Product not found")
        )

        with self.assertRaises(ProductNotFound):
            self.catalogue_service.delete_product(sku="invalidsku")


if __name__ == "__main__":
    unittest.main()
