import unittest
from unittest.mock import MagicMock
from uuid import uuid4

from src.adapter.dto import (
    CategoryDTO,
    InventoryDTO,
    PriceDTO,
    ProductRequestDTO,
    ProductResponseDTO,
)
from src.adapter.http_api import HTTPApiAdapter
from src.domain.entities import Category, Product
from src.domain.exceptions import InvalidSku, OutdatedProduct, ProductNotFound
from src.domain.services import CatalogueService
from src.domain.value_objects import Inventory, Price


class TestHTTPApiAdapter(unittest.TestCase):

    def setUp(self):
        self.mock_catalogue_service = MagicMock(spec=CatalogueService)
        self.adapter = HTTPApiAdapter(
            catalogue_service=self.mock_catalogue_service
        )

    def tearDown(self):
        self.mock_catalogue_service.reset_mock()

    def test_create_product_success(self):
        id_ = uuid4()
        mock_product_dto = ProductRequestDTO(
            sku="0123456789",
            name="Test Product",
            description="Test description",
            image_url="http://example.com/test.jpg",
            price=PriceDTO(value=10.0, discount_percent=0.1),
            inventory=InventoryDTO(quantity=100, reserved=10),
            category=CategoryDTO(name="Test Category"),
        )

        mock_created_product = Product(
            id=id_,
            sku="0123456789",
            name="Test Product",
            description="Test description",
            image_url="http://example.com/test.jpg",
            price=Price(value=10.0, discount_percent=0.1),
            inventory=Inventory(quantity=100, reserved=10),
            category=Category(name="Test Category"),
        )
        self.mock_catalogue_service.create_product.return_value = (
            mock_created_product
        )

        result = self.adapter.create_product(mock_product_dto)

        self.assertIsInstance(result, ProductResponseDTO)
        self.assertEqual(result.sku, mock_created_product.sku)
        self.assertEqual(result.name, mock_created_product.name)
        self.assertEqual(result.description, mock_created_product.description)
        self.assertEqual(result.image_url, mock_created_product.image_url)
        self.assertEqual(result.price.value, mock_created_product.price.value)
        self.assertEqual(
            result.price.discount_percent,
            mock_created_product.price.discount_percent,
        )
        self.assertEqual(
            result.inventory.quantity, mock_created_product.inventory.quantity
        )
        self.assertEqual(
            result.inventory.reserved, mock_created_product.inventory.reserved
        )
        self.assertEqual(
            result.category.name, mock_created_product.category.name
        )

        self.mock_catalogue_service.create_product.assert_called_once()
        call_args = self.mock_catalogue_service.create_product.call_args
        self.assertEqual(call_args[1]["sku"], mock_product_dto.sku)
        self.assertEqual(call_args[1]["name"], mock_product_dto.name)
        self.assertEqual(
            call_args[1]["description"], mock_product_dto.description
        )
        self.assertEqual(call_args[1]["image_url"], mock_product_dto.image_url)
        self.assertIsInstance(call_args[1]["price"], Price)
        self.assertIsInstance(call_args[1]["inventory"], Inventory)
        self.assertIsInstance(call_args[1]["category"], Category)

    def test_get_product_by_sku_success(self):
        id_ = uuid4()
        mock_product = Product(
            id=id_,
            sku="0123456789",
            name="Test Product",
            description="Test description",
            image_url="http://example.com/test.jpg",
        )
        self.mock_catalogue_service.get_product_by_sku.return_value = (
            mock_product
        )

        result = self.adapter.get_product_by_sku("0123456789")

        self.assertIsInstance(result, ProductResponseDTO)
        self.assertEqual(result.sku, mock_product.sku)
        self.assertEqual(result.name, mock_product.name)
        self.assertEqual(result.description, mock_product.description)
        self.assertEqual(result.image_url, mock_product.image_url)

        self.mock_catalogue_service.get_product_by_sku.assert_called_once_with(
            sku="0123456789"
        )

    def test_get_product_by_sku_invalid_sku(self):
        self.mock_catalogue_service.get_product_by_sku.side_effect = (
            InvalidSku("Invalid SKU")
        )

        with self.assertRaises(Exception):
            self.adapter.get_product_by_sku("0123456789")

        self.mock_catalogue_service.get_product_by_sku.assert_called_once_with(
            sku="0123456789"
        )

    def test_get_product_by_sku_product_not_found(self):
        self.mock_catalogue_service.get_product_by_sku.side_effect = (
            ProductNotFound("Product not found")
        )

        with self.assertRaises(Exception):
            self.adapter.get_product_by_sku("0123456789")

        self.mock_catalogue_service.get_product_by_sku.assert_called_once_with(
            sku="0123456789"
        )

    def test_update_product_success(self):
        id_ = uuid4()
        mock_product_dto = ProductRequestDTO(
            sku="0123456789",
            name="Updated Product",
            description="Updated description",
            image_url="http://example.com/updated.jpg",
            price=None,
            inventory=None,
            category=None,
        )

        mock_updated_product = Product(
            id=id_,
            sku="0123456789",
            name="Updated Product",
            description="Updated description",
            image_url="http://example.com/updated.jpg",
        )
        self.mock_catalogue_service.update_product.return_value = (
            mock_updated_product
        )

        result = self.adapter.update_product("0123456789", mock_product_dto)

        self.assertIsInstance(result, ProductResponseDTO)
        self.assertEqual(result.sku, mock_updated_product.sku)
        self.assertEqual(result.name, mock_updated_product.name)
        self.assertEqual(result.description, mock_updated_product.description)
        self.assertEqual(result.image_url, mock_updated_product.image_url)

        self.mock_catalogue_service.update_product.assert_called_once_with(
            sku="0123456789",
            name="Updated Product",
            description="Updated description",
            image_url="http://example.com/updated.jpg",
            price=None,
            inventory=None,
            category=None,
        )

    def test_update_product_invalid_sku(self):
        self.mock_catalogue_service.update_product.side_effect = InvalidSku(
            "Invalid SKU"
        )

        with self.assertRaises(Exception):
            self.adapter.update_product("0123456789", ProductRequestDTO())

    def test_update_product_product_not_found(self):
        self.mock_catalogue_service.update_product.side_effect = (
            ProductNotFound("Product not found")
        )

        with self.assertRaises(Exception):
            self.adapter.update_product("0123456789", ProductRequestDTO())

    def test_update_product_outdated_product(self):

        self.mock_catalogue_service.update_product.side_effect = (
            OutdatedProduct("Outdated product")
        )

        with self.assertRaises(Exception):
            self.adapter.update_product("0123456789", ProductRequestDTO())


if __name__ == "__main__":
    unittest.main()
