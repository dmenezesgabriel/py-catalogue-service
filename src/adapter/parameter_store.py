from typing import Optional

import boto3  # type: ignore
from src.port.parameter_store import ParameterStore


class SSMParameterStoreAdapter(ParameterStore):
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ) -> None:
        self.__session = boto3.Session()
        self.__credentials = self.__session.get_credentials()

        if not aws_access_key_id:
            aws_access_key_id = self.__credentials.access_key
        if not aws_secret_access_key:
            aws_secret_access_key = self.__credentials.secret_key

        self.__ssm = boto3.client(
            "ssm",
            endpoint_url=endpoint_url,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def get_parameter(self, name: str) -> str:
        response = self.__ssm.get_parameter(Name=name, WithDecryption=True)
        return response["Parameter"]["Value"]

    def get_database_url(self):
        return self.get_parameter(
            "/py-order-system-catalogue/postgres/catalogue/database_url"
        )
