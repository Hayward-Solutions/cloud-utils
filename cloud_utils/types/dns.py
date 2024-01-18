
class Zone:
    platform: str
    name: str
    domain: str
    id: str

    def __init__(self, platform: str, name: str, domain: str, id: str):
        self.platform = platform
        self.name = name
        self.domain = domain
        self.id = id


class Record:
    platform: str
    name: str
    zone: str
    record_type: str
    records: [str]

    def __init__(self, platform: str, name: str, zone: str, record_type: str, records: [str]):
        self.platform = platform
        self.name = name
        self.zone = zone
        self.record_type = record_type
        self.records = records
