
class Zone:
    platform: str
    name: str
    record_count: int
    zone_id: str

    def __init__(self, platform: str, name: str, record_count: int, zone_id: str):
        self.platform = platform
        self.name = name
        self.record_count = record_count
        self.zone_id = zone_id


class Record:
    platform: str
    name: str
    zone_id: str
    record_type: str
    records: [str]
    ttl: int

    def __init__(self, platform: str, name: str, zone_id: str, record_type: str, records: [str], ttl: int):
        self.platform = platform
        self.name = name
        self.zone_id = zone_id
        self.record_type = record_type
        self.records = records
        self.ttl = ttl
