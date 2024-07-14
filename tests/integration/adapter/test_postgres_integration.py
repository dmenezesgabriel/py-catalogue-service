import logging
import random
import unittest
from uuid import uuid4

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from src.adapter.exceptions import DatabaseException
from src.adapter.postgres import ProductPostgresAdapter
from src.config import get_config
from src.domain.entities import Category, Product
from src.domain.value_objects import Inventory, Price

config = get_config()
logger = logging.getLogger("app")


class TestProductPostgresAdapter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(config.DATABASE_URL)
        alembic_cfg = Config("migrations/alembic/alembic.ini")
        alembic_cfg.set_main_option("script_location", "migrations/alembic")
        alembic_cfg.attributes["connection"] = cls.engine.connect()
        command.upgrade(alembic_cfg, "head")

    @classmethod
    def tearDownClass(cls):
        alembic_cfg = Config("migrations/alembic/alembic.ini")
        alembic_cfg.set_main_option("script_location", "migrations/alembic")
        alembic_cfg.attributes["connection"] = cls.engine.connect()

        # command.downgrade(alembic_cfg, "base")

    def setUp(self):
        self.adapter = ProductPostgresAdapter(database_url=config.DATABASE_URL)

    def tearDown(self):
        pass

    def test_create_product(self):
        product_id = uuid4()
        price_id = uuid4()
        inventory_id = uuid4()
        category_id = uuid4()
        product_sku = str(random.randint(100, 1000))

        product = Product(
            id=product_id,
            version=0,
            sku=product_sku,
            name="Test Product",
            description="This is a test product",
            image_url="https://example.com/product.jpg",
            price=Price(id=price_id, value=99.99, discount_percent=0.1),
            inventory=Inventory(id=inventory_id, quantity=100, reserved=10),
            category=Category(id=category_id, name="Test Category"),
        )

        created_product = self.adapter.create_product(
            product=product,
            on_duplicate_sku=DatabaseException("Duplicate SKU"),
            on_not_found=DatabaseException("Product not found"),
        )

        retrieved_product = self.adapter.get_product_by_sku(
            sku=product_sku,
            on_not_found=DatabaseException("Product not found"),
        )

        self.assertIsNotNone(created_product)
        self.assertEqual(created_product.sku, product_sku)
        self.assertEqual(retrieved_product.sku, product_sku)

    def test_get_product_by_sku(self):
        product_id = uuid4()
        price_id = uuid4()
        inventory_id = uuid4()
        category_id = uuid4()
        product_sku = str(random.randint(100, 1000))

        product = Product(
            id=product_id,
            version=0,
            sku=product_sku,
            name="Test Product",
            description="This is a test product",
            image_url="https://example.com/product.jpg",
            price=Price(id=price_id, value=99.99, discount_percent=0.1),
            inventory=Inventory(id=inventory_id, quantity=100, reserved=10),
            category=Category(id=category_id, name="Test Category"),
        )

        self.adapter.create_product(
            product=product,
            on_duplicate_sku=DatabaseException("Duplicate SKU"),
            on_not_found=DatabaseException("Product not found"),
        )

        retrieved_product = self.adapter.get_product_by_sku(
            sku=product_sku,
            on_not_found=DatabaseException("Product not found"),
        )

        self.assertIsNotNone(retrieved_product)
        self.assertEqual(retrieved_product.sku, product_sku)
        self.assertEqual(retrieved_product.name, "Test Product")

    def test_update_product(self):
        product_id = uuid4()
        price_id = uuid4()
        inventory_id = uuid4()
        category_id = uuid4()
        new_category_id = uuid4()
        product_sku = str(random.randint(100, 1000))

        product = Product(
            id=product_id,
            version=0,
            sku=product_sku,
            name="Test Product 2",
            description="This is another test product",
            image_url="https://example.com/product2.jpg",
            price=Price(id=price_id, value=49.99, discount_percent=0.1),
            inventory=Inventory(id=inventory_id, quantity=50, reserved=5),
            category=Category(id=category_id, name="Test Category 2"),
        )

        self.adapter.create_product(
            product=product,
            on_duplicate_sku=DatabaseException("Duplicate SKU"),
            on_not_found=DatabaseException("Product not found"),
        )

        updated_product = Product(
            id=product_id,
            version=1,
            sku=product_sku,
            name="Updated Product Name",
            description="Updated description",
            image_url="https://example.com/updated_product.jpg",
            price=Price(id=price_id, value=59.99, discount_percent=0.1),
            inventory=Inventory(id=inventory_id, quantity=60, reserved=10),
            category=Category(id=new_category_id, name="Updated Category"),
        )

        updated_product_result = self.adapter.update_product(
            product=updated_product,
            on_not_found=DatabaseException("Product not found"),
            on_outdated_version=DatabaseException("Outdated version"),
            on_duplicate=DatabaseException("Duplicate product"),
        )

        retrieved_product = self.adapter.get_product_by_sku(
            sku=product_sku,
            on_not_found=DatabaseException("Product not found"),
        )

        self.assertIsNotNone(updated_product_result)
        self.assertEqual(updated_product_result.name, "Updated Product Name")
        self.assertEqual(retrieved_product.name, "Updated Product Name")

    def test_delete_product(self):
        product_id = uuid4()
        price_id = uuid4()
        inventory_id = uuid4()
        category_id = uuid4()
        product_sku = str(random.randint(100, 1000))

        product = Product(
            id=product_id,
            version=0,
            sku=product_sku,
            name="Product to Delete",
            description="This product will be deleted",
            image_url="https://example.com/delete_product.jpg",
            price=Price(id=price_id, value=29.99, discount_percent=0.1),
            inventory=Inventory(id=inventory_id, quantity=30, reserved=2),
            category=Category(id=category_id, name="Category to Delete"),
        )

        self.adapter.create_product(
            product=product,
            on_duplicate_sku=DatabaseException("Duplicate SKU"),
            on_not_found=DatabaseException("Product not found"),
        )

        delete_result = self.adapter.delete_product(
            sku=product_sku,
            on_not_found=DatabaseException("Product not found"),
        )

        with self.assertRaises(DatabaseException):
            self.adapter.get_product_by_sku(
                sku=product_sku,
                on_not_found=DatabaseException("Product not found"),
            )

        self.assertTrue(delete_result)


if __name__ == "__main__":
    unittest.main()
