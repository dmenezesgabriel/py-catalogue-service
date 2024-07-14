import logging
from typing import Optional

import boto3  # type: ignore
from src.adapter.exceptions import SqsException
from src.config import get_config
from src.domain.events import ProductEvent
from src.port.event_publishers import ProductEventPublisher

config = get_config()
logger = logging.getLogger("app")


class SQSAdapter(ProductEventPublisher):
    def __init__(
        self,
        queue_name: str,
        endpoint_url: Optional[str] = None,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ) -> None:
        self.__queue_name = queue_name
        self.__session = boto3.Session()
        self.__credentials = self.__session.get_credentials()

        if not aws_access_key_id:
            aws_access_key_id = self.__credentials.access_key
        if not aws_secret_access_key:
            aws_secret_access_key = self.__credentials.secret_key

        self.__sqs = boto3.client(
            "sqs",
            endpoint_url=endpoint_url,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def get_queue_url(self) -> str:
        try:
            response = self.__sqs.get_queue_url(QueueName=self.__queue_name)
            queue_url = response.get("QueueUrl")
            logger.debug(f"Got queue url: {queue_url}")
            return queue_url
        except Exception as error:
            raise SqsException(
                {
                    "code": "sqs.error.queue.unavailable",
                    "message": f"Sqs Queue not found {error}",
                }
            )

    def publish(self, product_event: ProductEvent) -> None:
        queue_url = self.get_queue_url()
        try:
            self.__sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=product_event.to_json(),
                DelaySeconds=0,
            )
        except Exception as error:
            raise SqsException(
                {
                    "code": "sqs.error.queue.send_message",
                    "message": f"Error sending message to sqs queue: {error}",
                }
            )
