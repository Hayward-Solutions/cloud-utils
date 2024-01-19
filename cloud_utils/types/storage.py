
class Bucket:
    platform: str
    name: str

    def __init__(self, name: str, platform: str):
        self.platform = platform
        self.name = name


class Blob:
    platform: str
    key: str
    bucket: str
    local_path: str

    def __init__(self, key: str, platform: str, bucket: str, local_path: str = ''):
        self.platform = platform
        self.key = key
        self.bucket = bucket
        self.local_path = local_path
