import unittest
from uuid import UUID, uuid4

from src.domain.entities import Category
from src.domain.exceptions import InvalidName


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.valid_name = "Valid Category"
        self.short_name = "No"
        self.empty_name = ""
        self.none_name = None
        self.valid_id = uuid4()

    def test_category_creation_with_id(self):
        category = Category(name=self.valid_name, id=self.valid_id)
        self.assertEqual(category.id, self.valid_id)
        self.assertEqual(category.name, self.valid_name)

    def test_category_creation_without_id(self):
        category = Category(name=self.valid_name)
        self.assertIsInstance(category.id, UUID)
        self.assertEqual(category.name, self.valid_name)

    def test_validate_name_valid(self):
        self.assertEqual(
            Category.validate_name(self.valid_name), self.valid_name
        )

    def test_validate_name_too_short(self):
        with self.assertRaises(InvalidName) as context:
            Category.validate_name(self.short_name)
        self.assertEqual(
            str(context.exception), "Name can not have less than 3 characters."
        )

    def test_validate_name_empty(self):
        with self.assertRaises(InvalidName) as context:
            Category.validate_name(self.empty_name)
        self.assertEqual(str(context.exception), "Name field is mandatory.")

    def test_validate_name_none(self):
        with self.assertRaises(InvalidName) as context:
            Category.validate_name(self.none_name)
        self.assertEqual(str(context.exception), "Name field is mandatory.")

    def test_to_dict(self):
        category = Category(name=self.valid_name, id=self.valid_id)
        expected_dict = {
            "id": str(self.valid_id),
            "name": self.valid_name,
        }
        self.assertEqual(category.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
