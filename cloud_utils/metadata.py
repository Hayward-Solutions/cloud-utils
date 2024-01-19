import requests
from cloud_utils.static.locations import Locations


class Metadata:
    platform: str
    location: str

    instance_id: str
    instance_name: str
    group_name: str
    region: str
    zone: str
    private_ip: str
    public_ip: str
    machine_type: str
    tags: dict

    project_id: str

    @staticmethod
    def get(url, google: bool = False) -> str:
        if google:
            headers = {'Metadata-Flavor': 'Google'}
        else:
            headers = {}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return ''

    @staticmethod
    def get_platform() -> str:
        try:
            code = requests.get('http://metadata.google.internal').status_code
        except Exception:
            pass
        else:
            if code == 200:
                return 'gcp'

        try:
            code = requests.get('http://169.254.169.254/latest/meta-data').status_code
        except Exception:
            pass
        else:
            if code == 200:
                return 'aws'

        return ''

    def get_location_from_region(self):
        if self.platform == 'aws':
            for location in Locations.aws:
                if Locations.aws[location] == self.region:
                    return location
        elif self.platform == 'gcp':
            for location in Locations.gcp:
                if Locations.gcp[location] == self.region:
                    return location

        print(f'ERROR deriving generic region from {self.platform} {self.region}')
        return None

    def __init__(self, platform: str = None):
        if platform is None:
            platform = self.get_platform()

        if platform.lower() not in ['aws', 'gcp']:
            print(f'Unable to derive metadata. This VM is not running in a valid cloud platform.')
            exit(0)

        if platform.lower() == 'aws':

            base_url = 'http://169.254.169.254/latest/meta-data/'
            self.project_id = ''
            self.platform = 'aws'
            self.instance_id = self.get(f'{base_url}/instance-id')
            self.instance_name = self.get(f'{base_url}/tags/instance/Name')
            self.group_name = self.get(f'{base_url}/tags/instance/aws:autoscaling:groupName')
            self.zone = self.get(f'{base_url}/placement/availability-zone')
            self.region = self.zone[:-1]
            self.private_ip = self.get(f'{base_url}/local-ipv4')
            self.public_ip = self.get(f'{base_url}/public-ipv4')
            self.machine_type = self.get(f'{base_url}/instance-type')
            self.tags = {}
            for tag in self.get(f'{base_url}/tags/instance/').split('\n'):
                self.tags[tag] = self.get(f'{base_url}/tags/instance/{tag}')

        elif platform.lower() == 'gcp':

            base_url = 'http://metadata.google.internal/computeMetadata/v1'

            self.platform = 'gcp'
            self.project_id = self.get(f'{base_url}/project/project-id', google=True)
            self.instance_id = self.get(f'{base_url}/instance/id', google=True)
            self.instance_name = self.get(f'{base_url}/instance/name', google=True)
            self.group_name = self.get(f'{base_url}/instance/attributes/created-by', google=True)
            self.zone = self.get(f'{base_url}/instance/zone', google=True)
            self.region = self.zone.split('/')[-1]
            self.private_ip = self.get(f'{base_url}/instance/network-interfaces/0/ip', google=True)
            self.public_ip = self.get(f'{base_url}/instance/network-interfaces/0/access-configs/0/external-ip', google=True)
            self.machine_type = self.get(f'{base_url}/instance/machine-type', google=True).split('/')[-1]
            self.tags = {}

        self.location = self.get_location_from_region()
