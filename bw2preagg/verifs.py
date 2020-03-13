"""Set of functions used to verify output

Used by tests and in EDA
"""
from presamples.campaigns import Campaign, PresampleResource

def get_indices_and_samples_from_campaign(campaign_name):
    """Return actual indices and samples form campaign name"""
    # Load campaign
    c = Campaign.get_or_none(Campaign.name==campaign_name)

    if c is None:
        raise ValueError("No campaign named {}".format(campaign_name))
    if len(c) == 0:
        raise ValueError("{} is empty".format(campaign_name))
    indices = {}
    samples = {}
    for p in c:
        resource = PresampleResource.get(PresampleResource.path == p)

def check_presample_size():
    pass