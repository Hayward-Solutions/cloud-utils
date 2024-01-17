
class Locations:
    """
    Defines a static map of cloud-agnostic locations to provider specific locations.
    """
    aws = {
        'london': 'eu-west-2',
        'ireland': 'eu-west-1'
    }
    gcp = {
        'london': 'europe-west2',
        'ireland': 'europe-west1'
    }
