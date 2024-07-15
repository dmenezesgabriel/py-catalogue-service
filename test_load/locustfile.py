import logging
import random
import string

from locust import HttpUser, between, task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductApiUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks
    product_sku = None  # Track the SKU of the created product

    def on_start(self) -> None:
        """Run on start"""
        self.sku = self.generate_sku()
        self.product_data = {
            "sku": self.sku,
            "name": "Test Product",
            "description": "This is a test product",
            "image_url": "http://example.com/image.jpg",
            "price": {"value": 100.0, "discount_percent": 0.1},
            "inventory": {"quantity": 50, "reserved": 5},
            "category": {"name": "Test Category"},
        }

    def generate_sku(self, length=8) -> str:
        """Generate a random SKU"""
        return "".join(
            random.choices(string.ascii_uppercase + string.digits, k=length)
        )

    @task(1)
    def create_product(self) -> None:
        response = self.client.post("/product", json=self.product_data)
        if not response.status_code == 200:
            logger.info(f"Failed to create product: {response.json()}")
            return None
        self.product_sku = self.sku  # Store the SKU of the created product

    @task(2)
    def get_product(self) -> None:
        if not self.product_sku:
            logger.info("No product SKU available for retrieval")
            return None
        response = self.client.get(f"/product/{self.product_sku}")
        if not response.status_code == 200:
            logger.info(f"Failed to retrieve product: {response.json()}")
            return None

    @task(3)
    def update_product(self) -> None:
        if not self.product_sku:
            logger.info("No product SKU available for update")
            return None
        updated_data = self.product_data.copy()
        updated_data["name"] = "Updated Product Name"
        response = self.client.put(
            f"/product/{self.product_sku}", json=updated_data
        )
        if not response.status_code == 200:
            logger.info(f"Failed to update product: {response.json()}")
            return None

    @task(1)
    def delete_product(self) -> None:
        if not self.product_sku:
            logger.info("No product SKU available for deletion")
            return None
        response = self.client.delete(f"/product/{self.product_sku}")
        if not response.status_code == 200:
            logger.info(f"Failed to delete product: {response.json()}")
            return None
        self.product_sku = None  # Reset the SKU after deletion

    def on_stop(self) -> None:
        """Clean up product on stop"""
        if self.product_sku:
            self.client.delete(f"/product/{self.product_sku}")
