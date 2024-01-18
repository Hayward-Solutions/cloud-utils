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
                 secret_key: str = None):

        self.region = region

        if profile:
            self.session = boto3.session.Session(profile_name=profile, region_name=region)
        elif session_token and access_key and secret_key:
            self.session = self.boto_session(access_key, secret_key, session_token, region)
        else:
            raise 'One of [profile] or [access_key, secret_key, session_token] must be provided.'

    @staticmethod
    def boto_session(access_key, secret_key, session_token, region):
        return boto3.session.Session(
            aws_session_token=session_token,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
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
