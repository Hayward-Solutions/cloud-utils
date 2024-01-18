import boto3
import botocore.exceptions

from cloud_utils.cloud_clients.apis.aws.compute import Compute
from cloud_utils.cloud_clients.apis.aws.dns import Dns


class AWS:
    session = None
    region: str

    dns = Dns
    compute = Compute

    def __init__(self,
                 region: str,
                 profile: str = None,
                 session_token: str = None,
                 access_key: str = None,
                 secret_key: str = None,
                 load_host_credentials: bool = False,
                 role_arn: str = None):

        self.region = region

        if load_host_credentials:
            self.session = boto3.session.Session()
        elif profile or all([access_key, secret_key, session_token]):
            self.session = boto3.session.Session(
                profile_name=profile,
                region_name=region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                aws_session_token=session_token,
            )
        else:
            print('ERROR: Invalid client credentials options')
            print('ERROR: Valid options are:')
            print('ERROR:       [load_host_credentials] + Optional[role_arn]')
            print('ERROR:       [profile] + Optional[role_arn]')
            print('ERROR:       [access_key, secret_key, session_token] + Optional[role_arn]')
            raise Exception

        if role_arn:
            try:
                sts = self.session.client('sts')
                credentials = sts.assume_role(RoleArn=role_arn, RoleSessionName='cloud-utils')['Credentials']
            except botocore.exceptions.ClientError:
                print(f'ERROR: Failed to assume role {role_arn}')
                raise
            else:
                self.session = boto3.session.Session(
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken'],
                    region_name=region
                )

        self.compute = Compute(self.session)
        self.dns = Dns(self.session)
