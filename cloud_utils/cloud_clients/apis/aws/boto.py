import boto3
import botocore.exceptions


def boto_client(client_session, service: str):
    try:
        return client_session.client(service_name=service)
    except botocore.exceptions.ClientError:
        raise
