import boto3
import botocore.exceptions
from cloud_utils.types.compute import InstanceGroup
from cloud_utils.types.compute import Instance


class AWS:
    session = None
    region: str

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

    def boto_client(self, service: str):
        try:
            return self.session.client(service_name=service)
        except botocore.exceptions.ClientError:
            raise

    def get_groups(self, group_name: str = None) -> [InstanceGroup]:
        autoscaling = self.boto_client('autoscaling')
        if group_name:
            response = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])
        else:
            response = autoscaling.describe_auto_scaling_groups()

        groups = []
        for asg in response['AutoScalingGroups']:
            groups.append(InstanceGroup(
                name=asg['AutoScalingGroupName'],
                platform='AWS',
                size=asg['DesiredCapacity'],
                instance_ids=[instance['InstanceId'] for instance in asg['Instances']]
            ))

        return groups

    def get_instances(self, group_name: str = None, identifier: str = None) -> [Instance]:
        if not identifier:
            instance_groups = self.get_groups(group_name=group_name)

            instance_ids = []
            for group in instance_groups:
                instance_ids += group.instance_ids

            if len(instance_ids) == 0:
                return []
        else:
            instance_ids = [identifier]

        ec2 = self.boto_client('ec2')
        try:
            response = ec2.describe_instances(InstanceIds=instance_ids)
        except botocore.exceptions.ClientError:
            raise
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                name_tag = [tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'][0]
                instances.append(Instance(
                    platform='AWS',
                    instance_group=name_tag,
                    identifier=instance['InstanceId'],
                    instance_type=instance['InstanceType'],
                    zone=instance['Placement']['AvailabilityZone'],
                    status=instance['State']['Name'],
                    private_ip=None if 'PrivateIpAddress' not in instance else instance['PrivateIpAddress'],
                    public_ip=None if 'PublicIpAddress' not in instance else instance['PublicIpAddress']
                ))

        return instances

    def scale(self, group_name: str, size: int):
        autoscaling = self.boto_client('autoscaling')
        autoscaling.set_desired_capacity(
            AutoScalingGroupName=group_name,
            DesiredCapacity=size
        )
