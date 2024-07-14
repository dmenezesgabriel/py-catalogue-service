import unittest
from unittest.mock import patch

import boto3  # type: ignore
from moto import mock_aws
from src.adapter.exceptions import SqsException
from src.adapter.sqs import SQSAdapter
from src.domain.enums import ProductEventType
from src.domain.events import ProductEvent


@mock_aws
class TestSQSAdapter(unittest.TestCase):

    @patch("src.adapter.sqs.boto3")
    def setUp(self, mock_boto3):
        self.mock_boto3 = mock_boto3
        self.sqs_client = boto3.client("sqs", region_name="us-east-1")

        self.queue_name = "product-update"
        sqs_queue = self.sqs_client.create_queue(QueueName=self.queue_name)
        self.queue_url = sqs_queue["QueueUrl"]

        self.mock_boto3.client.return_value = self.sqs_client
        self.adapter = SQSAdapter(
            queue_name=self.queue_name,
            region_name="us-east-1",
        )

    def tearDown(self):
        pass

    def test_publish_success(self):
        product_event = ProductEvent(
            type=ProductEventType.DELETED, product=None, sku="0123456789"
        )

        self.adapter.publish(product_event)
        response = self.sqs_client.receive_message(
            QueueUrl=self.queue_url, WaitTimeSeconds=0
        )
        messages = response.get("Messages", [])

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["Body"], product_event.to_json())

    def test_publish_sqs_error(self):
        product_event = ProductEvent(type="created", product=None)

        with self.assertRaises(SqsException):
            self.adapter.publish(product_event)

    def test_publish_queue_not_found(self):
        product_event = ProductEvent(type="created", product=None)

        with self.assertRaises(SqsException):
            self.adapter.publish(product_event)


if __name__ == "__main__":
    unittest.main()
