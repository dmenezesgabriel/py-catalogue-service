import base64
import unittest
from unittest.mock import patch

from src.utils.singleton import Singleton, SingletonHash, generate_hash


class SingletonClass(metaclass=Singleton):
    pass


class SingletonHashClass(metaclass=SingletonHash):
    def __init__(self, value):
        self.value = value


class TestGenerateHash(unittest.TestCase):
    def test_generate_hash(self):
        value = "test_value"
        expected_hash = base64.b64encode(value.encode("ascii")).decode("utf8")
        self.assertEqual(generate_hash(value), expected_hash)


class TestSingleton(unittest.TestCase):
    def setUp(self):
        Singleton.drop()  # Ensure a clean state before each test

    def test_singleton_instance(self):
        instance1 = SingletonClass()
        instance2 = SingletonClass()
        self.assertIs(
            instance1, instance2, "Singleton did not return the same instance"
        )

    def test_singleton_drop(self):
        instance1 = SingletonClass()
        Singleton.drop()
        instance2 = SingletonClass()
        self.assertIsNot(
            instance1,
            instance2,
            "Singleton did not reset the instances correctly",
        )


class TestSingletonHash(unittest.TestCase):
    def setUp(self):
        SingletonHash.drop()  # Ensure a clean state before each test

    def test_singleton_hash_instance(self):
        instance1 = SingletonHashClass(value="test")
        instance2 = SingletonHashClass(value="test")
        self.assertIs(
            instance1,
            instance2,
            "SingletonHash did not return the same instance for same hash",
        )

        instance3 = SingletonHashClass(value="test2")
        self.assertIsNot(
            instance1,
            instance3,
            "SingletonHash returned the same instance for different hash",
        )

    def test_singleton_hash_drop(self):
        instance1 = SingletonHashClass(value="test")
        SingletonHash.drop()
        instance2 = SingletonHashClass(value="test")
        self.assertIsNot(
            instance1,
            instance2,
            "SingletonHash did not reset the instances correctly",
        )

    @patch("src.utils.singleton.generate_hash")
    def test_singleton_hash_generate_hash(self, mock_generate_hash):
        mock_generate_hash.side_effect = lambda x: "mocked_hash_" + x
        SingletonHashClass(value="test")
        mock_generate_hash.assert_called_with("(){'value': 'test'}")
        self.assertEqual(
            len(SingletonHash._instances),
            1,
            "SingletonHash did not store the instance correctly with hash",
        )


if __name__ == "__main__":
    unittest.main()
