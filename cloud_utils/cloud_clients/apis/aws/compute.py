import boto3
import botocore.exceptions
from cloud_utils.types.compute import InstanceGroup
from cloud_utils.types.compute import Instance
from cloud_utils.cloud_clients.apis.aws.boto import boto_client


class Compute:
    session = boto3.session.Session

    def __init__(self, session: boto3.session.Session):
        self.session = session

    def get_groups(self, group_name: str = None) -> [InstanceGroup]:
        autoscaling = boto_client(self.session, 'autoscaling')
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

        ec2 = boto_client(self.session, 'ec2')
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
        autoscaling = boto_client(self.session, 'autoscaling')
        autoscaling.set_desired_capacity(
            AutoScalingGroupName=group_name,
            DesiredCapacity=size
        )
