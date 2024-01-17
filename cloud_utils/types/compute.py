
class Instance:
    platform: str
    instance_group: str
    identifier: str
    status: str
    instance_type: str
    public_ip: str
    private_ip: str
    zone: str

    def __init__(self,
                 platform: str,
                 instance_group: str,
                 identifier: str,
                 status: str,
                 instance_type: str,
                 zone: str,
                 public_ip: str = None,
                 private_ip: str = None):

        self.platform = platform
        self.instance_group = instance_group
        self.identifier = identifier
        self.status = status
        self.instance_type = instance_type
        self.zone = zone
        self.public_ip = public_ip
        self.private_ip = private_ip


class InstanceGroup:
    name: str
    platform: str
    size: int
    instance_ids: list[str]

    def __init__(self,
                 name: str,
                 platform: str,
                 size: int,
                 instance_ids: list[str]):
        self.name = name
        self.platform = platform
        self.size = size
        self.instance_ids = instance_ids
