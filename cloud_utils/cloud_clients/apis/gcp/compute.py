from google.cloud import compute
from google.api_core.exceptions import NotFound
from cloud_utils.types.compute import InstanceGroup
from cloud_utils.types.compute import Instance


class Compute:
    project: str
    region: str

    def __init__(self, project: str, region: str):
        self.project = project
        self.region = region

    def get_groups(self, group_name: str = None) -> [InstanceGroup]:
        compute_client = compute.RegionInstanceGroupsClient()
        instance_groups = compute_client.list(project=self.project, region=self.region)
        groups = []
        for mig in instance_groups:
            if group_name is None or group_name == mig.name:
                instances = compute_client.list_instances(instance_group=mig.name, project=self.project, region=self.region)
                instance_ids = [instance.instance.split('/')[-1] for instance in instances]
                groups.append(InstanceGroup(
                    platform='GCP',
                    name=mig.name,
                    size=mig.size,
                    instance_ids=instance_ids
                ))
        return groups

    def get_instances(self, group_name: str = None, identifier: str = None) -> [Instance]:
        def process_instance(gcp_instance) -> Instance:
            internal_ips = []
            external_ips = []
            for interface in gcp_instance.network_interfaces:
                internal_ips.append(interface.network_i_p)
                for access_config in interface.access_configs:
                    external_ips.append(access_config.nat_i_p)

            return Instance(
                platform='GCP',
                instance_group=gcp_instance.labels["name"],
                identifier=gcp_instance.name,
                zone=gcp_instance.zone.split('/')[-1],
                instance_type=gcp_instance.machine_type.split('/')[-1],
                status=gcp_instance.status.lower(),
                private_ip=None if len(internal_ips) == 0 else internal_ips[0],
                public_ip=None if len(external_ips) == 0 else external_ips[0],
            )

        compute_client = compute.InstancesClient()
        zones = [f'{self.region}-{zone}' for zone in ['a', 'b', 'c']]
        vms = []
        for zone in zones:
            if identifier:
                try:
                    instance = compute_client.get(project=self.project, zone=zone, instance=identifier)
                except NotFound:
                    pass
                else:
                    vms.append(process_instance(instance))
            else:
                instances = compute_client.list(project=self.project, zone=zone)
                for instance in instances:
                    if group_name is None or group_name in instance.name:
                        vms.append(process_instance(instance))

        return vms

    def scale(self, group_name: str, size: int):
        compute_client = compute.RegionInstanceGroupManagersClient()
        compute_client.resize(
            project=self.project, region=self.region, instance_group_manager=group_name, size=size
        )

